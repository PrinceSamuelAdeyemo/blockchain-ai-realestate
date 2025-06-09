from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ContractEventViewSet,
    SmartContractViewSet,
    GasFeeRecordViewSet
)

router = DefaultRouter()
router.register(r'contracts', SmartContractViewSet, basename='smartcontract')
router.register(r'events', ContractEventViewSet, basename='contractevent')
router.register(r'gas-fees', GasFeeRecordViewSet, basename='gasfee')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
