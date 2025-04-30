from django.contrib import admin
from .models import ModelVersion, Prediction, TrainingData, FeatureSet

# Register your models here.
admin.site.register([
    ModelVersion,
    Prediction,
    TrainingData,
    FeatureSet
])