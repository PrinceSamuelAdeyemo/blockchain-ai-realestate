from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PropertyViewSet,
    PropertyTypeViewSet,
    AmenityViewSet,
    PropertyImageViewSet,   
    PropertyDocumentViewSet,
    predict_price,
    load_model_and_predict
)

router = DefaultRouter()

router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'property-types', PropertyTypeViewSet, basename='property-type')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'property-images', PropertyImageViewSet, basename='property-image')
router.register(r'property-documents', PropertyDocumentViewSet, basename='property-document')

urlpatterns = [
    path('api/v1/predict/', predict_price, name='predict_price'),
    path('api/v1/load_model_and_predict/', load_model_and_predict, name='load_model_and_predict'),
    path('api/v1/', include(router.urls)),
]
    
    