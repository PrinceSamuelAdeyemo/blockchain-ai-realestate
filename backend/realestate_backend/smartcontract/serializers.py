from rest_framework import serializers
from .models import (
    ContractEvent,
    SmartContract,
    GasFeeRecord
)


class ContractEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractEvent
        fields = '__all__'
        
        
class SmartContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartContract
        fields = '__all__'
        
        
class GasFeeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasFeeRecord
        fields = '__all__'
        