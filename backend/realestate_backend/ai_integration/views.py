from django.shortcuts import render

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