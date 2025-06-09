from django.contrib import admin
from .models import ModelVersion, Prediction, TrainingData, FeatureSet
from django.utils.translation import gettext_lazy as _

# Register your models here.
#admin.site.site_header = "Real Estate AI Integration Admin"
#admin.site.site_title = "Real Estate AI Integration Admin Portal"
#admin.site.index_title = "Welcome to the Real Estate AI Integration Admin Portal"

admin.site.register([
    # Add your models here
    ModelVersion,
    Prediction,
    TrainingData,
    FeatureSet,
])