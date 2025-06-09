from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    ContractEvent, 
    SmartContract,
    GasFeeRecord
)
from .serializers import (
    ContractEventSerializer,
    SmartContractSerializer, 
    GasFeeRecordSerializer
)

# Create your views here.
class ContractEventViewSet(viewsets.ModelViewSet):
    queryset = ContractEvent
    serializer_class = ContractEventSerializer
    
    
class SmartContractViewSet(viewsets.ModelViewSet):
    queryset = SmartContract
    serializer_class = SmartContractSerializer
    
    
class GasFeeRecordViewSet(viewsets.ModelViewSet):
    queryset = GasFeeRecord
    serializer_class = GasFeeRecordSerializer