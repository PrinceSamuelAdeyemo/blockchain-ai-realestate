from django.shortcuts import render
import pickle
from sklearn.preprocessing import LabelEncoder
from django.views.decorators.csrf import csrf_exempt
import os
import pandas as pd
import joblib

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ModelVersion, Prediction, TrainingData, FeatureSet
from .serializers import (
    ModelVersionSerializer,
    PredictionSerializer,
    TrainingDataSerializer,
    FeatureSetSerializer
)


class ModelVersionViewSet(viewsets.ModelViewSet):
    queryset = ModelVersion.objects.all()
    serializer_class = ModelVersionSerializer
    permission_classes = [IsAuthenticated]


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]


class TrainingDataViewSet(viewsets.ModelViewSet):
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer
    permission_classes = [IsAuthenticated]
    

class FeatureSetViewSet(viewsets.ModelViewSet):
    queryset = FeatureSet.objects.all()
    serializer_class = FeatureSetSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ai_integration.train_and_register_model import load_model_and_predict

@api_view(["POST"])
def predict_price(request):
    """
    API endpoint to predict real estate prices using the trained model.
    """
    input_data = request.data
    le = LabelEncoder()
    input_data['country_encoded'] = le.transform([input_data['country_encoded']])[0]
    print(input_data)


    try:
        # Make predictions
        predictions = load_model_and_predict(input_data)
        print("prediction", predictions)
        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)
    except FileNotFoundError as e:
        print("File error", str(e))
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        print("error here", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
def load_model_and_predict(request):
    #Load the trained model and make predictions on the input data.
    raw_data = request.data
    input_data = {
        key: float(raw_data[key][0] if isinstance(raw_data[key], list) else raw_data[key])
        for key in raw_data
    }
    # Load the trained model
    model_path = 'xgboost_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model file not found. Please train the model first.")

    model = joblib.load(model_path)

    print(input_data)
    # Convert input data to DataFrame if it's a dictionary
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Ensure input data has the same features as the training data
    required_features = [
        'apartment_total_area', 'apartment_living_area', 'apartment_rooms',
        'apartment_bedrooms', 'apartment_bathrooms', 'building_age',
        'building_total_floors', 'apartment_floor', 'country_encoded',
        'price_per_sqm'
    ]
    #missing_features = [feature for feature in required_features if feature not in input_data]
    #if missing_features:
    #    raise ValueError(f"Missing required features: {missing_features}")

    # Make predictions
    predictions = model.predict(input_data)
    return Response({"predictions": predictions})
    #return predictions