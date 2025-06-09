from django.core.management.base import BaseCommand
from ai_integration.models import ModelVersion, FeatureSet, TrainingData

import pandas as pd
import numpy as np
import joblib
import hashlib
import os
import re
from datetime import datetime

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb


class Command(BaseCommand):
    help = "Train and register a real estate price model"

    def handle(self, *args, **kwargs):
        dataset_path = os.path.abspath("ai_integration/datasets/world_real_estate_data(147k).csv")
        df = pd.read_csv(dataset_path)
        df_processed = self.preprocess_data(df)
        X, y = self.select_features(df_processed)

        # Train model
        best_model, grid_search, y_test, y_pred = self.train_xgboost(X, y)

        # Save model
        model_path = 'apartment_price_model.json'
        best_model.named_steps['xgb'].save_model(model_path)

        # Register in DB
        self.register_model(best_model, grid_search, X, y, model_path, dataset_path)

        # Show final results
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mean_price = y_test.mean()
        accuracy = max(0, 1 - rmse / mean_price)

        self.stdout.write(self.style.SUCCESS("✅ Model Training Complete"))
        self.stdout.write(f"Best Parameters: {grid_search.best_params_}")
        self.stdout.write(f"RMSE: {rmse:.2f}")
        self.stdout.write(f"R² Score: {r2:.2f}")
        self.stdout.write(f"Mean Price: {mean_price:.2f}")
        self.stdout.write(f"Approximate Accuracy: {accuracy * 100:.2f}%")

    def preprocess_data(self, df):
        df = df.copy()
        mask = df['title'].str.contains(r'^\d+\s*room', na=False, regex=True)
        df = df.loc[mask].copy()
        df['title_rooms'] = df['title'].str.extract(r'^(\d+)\s*room')[0].astype(float)

        area_cols = ['apartment_total_area', 'apartment_living_area']
        for col in area_cols:
            df[col] = df[col].str.extract(r'(\d+)', expand=False).astype(float)

        df['apartment_rooms'] = df['apartment_rooms'].fillna(df['title_rooms'])
        df = df.dropna(subset=['price_in_USD', 'apartment_total_area', 'country'])

        numeric_cols = ['apartment_bedrooms', 'apartment_bathrooms', 'apartment_living_area',
                        'building_total_floors', 'apartment_floor', 'building_construction_year']
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        df['building_age'] = pd.Timestamp.now().year - df['building_construction_year']
        df['price_per_sqm'] = df['price_in_USD'] / df['apartment_total_area']

        le = LabelEncoder()
        df['country_encoded'] = le.fit_transform(df['country'])

        # Outlier filtering
        df = df[
            (df['price_in_USD'].between(df['price_in_USD'].quantile(0.01), df['price_in_USD'].quantile(0.99))) &
            (df['apartment_total_area'].between(df['apartment_total_area'].quantile(0.01), df['apartment_total_area'].quantile(0.99)))
        ]

        return df

    def select_features(self, df):
        features = [
            'apartment_total_area',
            'apartment_living_area',
            'apartment_rooms',
            'apartment_bedrooms',
            'apartment_bathrooms',
            'building_age',
            'building_total_floors',
            'apartment_floor',
            'country_encoded',
            'price_per_sqm'
        ]
        return df[features], df['price_in_USD']

    def train_xgboost(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('xgb', xgb.XGBRegressor(objective='reg:squarederror'))
        ])

        param_grid = {
            'xgb__max_depth': [4, 6, 8],
            'xgb__learning_rate': [0.01, 0.1, 0.2],
            'xgb__n_estimators': [100, 200, 300],
            'xgb__colsample_bytree': [0.6, 0.8, 1.0],
            'xgb__subsample': [0.6, 0.8, 1.0]
        }

        grid_search = GridSearchCV(
            pipeline,
            param_grid,
            cv=5,
            scoring='neg_root_mean_squared_error',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        y_pred = best_model.predict(X_test)

        return best_model, grid_search, y_test, y_pred

    def register_model(self, model, grid, X, y, model_path, dataset_path):
        with open(model_path, 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()

        training_data = TrainingData.objects.create(
            name="Global Real Estate",
            version="v1.0",
            data_type="STRUCTURED",
            storage_location=dataset_path,
            size_gb=round(os.path.getsize(dataset_path) / (1024**3), 2),
            record_count=len(X),
            date_range_start=datetime(2021, 1, 1),
            date_range_end=datetime(2024, 1, 1),
            geographic_scope={"countries": ["All"], "cities": []},
            data_schema=X.dtypes.astype(str).to_dict()
        )

        feature_set = FeatureSet.objects.create(
            name="ValuationFeatures",
            version="v1.0",
            features=[{"name": col, "type": "numerical", "source": "user", "description": ""} for col in X.columns],
            transformations=[],
        )
        feature_set.required_data.add(training_data)

        ModelVersion.objects.create(
            model_type="VALUATION",
            version="v1.0",
            framework="XGBOOST",
            storage_path=model_path,
            checksum=checksum,
            is_production=True,
            training_data=training_data,
            feature_set=feature_set,
            hyperparameters=grid.best_params_,
            metrics={
                "rmse": round(mean_squared_error(y, model.predict(X))**0.5, 2),
                "r2": round(r2_score(y, model.predict(X)), 4)
            }
        )
