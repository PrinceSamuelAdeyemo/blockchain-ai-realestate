from django.shortcuts import render
from rest_framework import viewsets
from .serializers import (
    LeaseSerializer, 
    TenantSerializer,
    MaintenanceRequestSerializer,
    InspectionSerializer
)
from .models import (
    Lease, 
    Tenant,
    MaintenanceRequest,
    Inspection
)
# Create your views here.

class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    
    
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    
    
class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    
    
class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer