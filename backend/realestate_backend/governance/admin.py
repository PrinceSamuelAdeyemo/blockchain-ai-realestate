from django.contrib import admin
from .models import ModelVersion, Prediction, TrainingData, FeatureSet
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register([
    ModelVersion,
    Prediction,
    TrainingData,
    FeatureSet
])