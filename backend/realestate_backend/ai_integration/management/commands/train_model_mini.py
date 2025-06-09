from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
import joblib
import hashlib
import os
from datetime import datetime

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import xgboost as xgb

from ai_integration.models import ModelVersion, FeatureSet, TrainingData


class Command(BaseCommand):
    help = 'Train and register an XGBoost model for real estate valuation'

    def handle(self, *args, **kwargs):
        dataset_path = os.path.abspath("ai_integration/datasets/world_real_estate_data(147k).csv")
        print(dataset_path)
        df = pd.read_csv(dataset_path)
        df = self.preprocess_data(df)
        X, y = self.select_features(df)

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('xgb', xgb.XGBRegressor(objective='reg:squarederror'))
        ])

        param_grid = {
            'xgb__max_depth': [4, 6],
            'xgb__learning_rate': [0.05, 0.1],
            'xgb__n_estimators': [100, 200],
            'xgb__colsample_bytree': [0.6, 0.8],
            'xgb__subsample': [0.8, 1.0]
        }

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        grid = GridSearchCV(pipeline, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1, verbose=1)
        grid.fit(X_train, y_train)

        best_model = grid.best_estimator_
        self.register_model(best_model, grid, X, y, dataset_path)

        self.stdout.write(self.style.SUCCESS("✅ Model training and registration complete."))

    def preprocess_data(self, df):
        df = df.copy()
        mask = df['title'].str.contains(r'^\d+\s*room', na=False, regex=True)
        df = df.loc[mask].copy()
        df['title_rooms'] = df['title'].str.extract(r'^(\d+)\s*room')[0].astype(float)

        for col in ['apartment_total_area', 'apartment_living_area']:
            df[col] = df[col].str.extract(r'(\d+)', expand=False).astype(float)

        df['apartment_rooms'] = df['apartment_rooms'].fillna(df['title_rooms'])
        df = df.dropna(subset=['price_in_USD', 'apartment_total_area', 'country'])

        numeric_cols = ['apartment_bedrooms', 'apartment_bathrooms', 'apartment_living_area',
                        'building_total_floors', 'apartment_floor', 'building_construction_year']
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        df['building_age'] = datetime.now().year - df['building_construction_year']
        df['price_per_sqm'] = df['price_in_USD'] / df['apartment_total_area']

        le = LabelEncoder()
        df['country_encoded'] = le.fit_transform(df['country'])
        print(f"Encoded countries: {dict(zip(le.classes_, le.transform(le.classes_)))}")
        print(f"Number of unique countries: {len(le.classes_)}")
        print(f"country: {df['country'].unique()}", "country_encoded:", df['country_encoded'].unique())

        return df

    def select_features(self, df):
        features = [
            'apartment_total_area', 'apartment_living_area', 'apartment_rooms',
            'apartment_bedrooms', 'apartment_bathrooms', 'building_age',
            'building_total_floors', 'apartment_floor', 'country_encoded',
            'price_per_sqm'
        ]
        X = df[features]
        y = df['price_in_USD']
        return X, y

    def register_model(self, model, grid, X, y, dataset_path):
        model_path = 'xgboost_model.pkl'
        joblib.dump(model, model_path)

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
            metrics={"rmse": round(mean_squared_error(y, model.predict(X))**0.5, 2)},
        )
