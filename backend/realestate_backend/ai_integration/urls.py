from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
from .views import (
    ModelVersionViewSet,
    PredictionViewSet,
    TrainingDataViewSet,
    FeatureSetViewSet,
    predict_price,
    load_model_and_predict,
)
# Register the viewsets with the router
router.register(r'model_versions', ModelVersionViewSet, basename='modelversion')
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'training_data', TrainingDataViewSet, basename='trainingdata')
router.register(r'feature_sets', FeatureSetViewSet, basename='featureset')

urlpatterns = [
    path('api/v1/predict/', load_model_and_predict, name='predict_price'),
    path('api/v1/', include(router.urls)),
]
