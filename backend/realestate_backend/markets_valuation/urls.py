from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ValuationViewSet,
    MarketTrendViewSet,
    PriceHistoryViewSet,
    NeighborhoodDataViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'valuations', ValuationViewSet)
router.register(r'market-trends', MarketTrendViewSet)
router.register(r'price-history', PriceHistoryViewSet)
router.register(r'neighborhood-data', NeighborhoodDataViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    # Add any additional URLs here if needed
]
