from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LeaseViewSet,
    TenantViewSet,
    MaintenanceRequestViewSet,
    InspectionViewSet,
    #Payment
)

router = DefaultRouter()
router.register(r'leases', LeaseViewSet, basename='lease')
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'maintenance_requests', MaintenanceRequestViewSet, basename='maintenance_request')
router.register(r'inspections', InspectionViewSet, basename='inspection')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    # path('payments/', Payment.as_view(), name='payment'
]
