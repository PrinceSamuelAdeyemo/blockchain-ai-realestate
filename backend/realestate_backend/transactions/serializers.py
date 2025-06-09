from rest_framework import serializers
from .models import (
    Investment,
    DividendPayout,
    Transaction,
    Escrow
    )


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
        
        
class DividendPayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendPayout
        fields = '__all__'
        
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        
        
class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = '__all__'