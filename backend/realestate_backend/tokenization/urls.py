from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TokenizedAssetViewSet,
    TokenOwnershipViewSet,
    FractionalOwnershipViewset,
    TokenTransactionViewSet
)

router = DefaultRouter()
router.register(r'tokenized-assets', TokenizedAssetViewSet, basename='tokenizedasset')
router.register(r'token-ownership', TokenOwnershipViewSet, basename='tokenownership')
router.register(r'fractional-ownership', FractionalOwnershipViewset, basename='fractionalownership')
router.register(r'token-transactions', TokenTransactionViewSet, basename='tokentransaction')

urlpatterns = [
    path('api/v1/', include(router.urls))
]
