from rest_framework import serializers
from .models import (
    TokenizedAsset,
    TokenOwnership,
    FractionalOwnership,
    TokenTransaction
)


class TokenizedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenizedAsset
        fields = '__all__'
        
        
class TokenOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenOwnership
        fields = '__all__'
        
        
class FractionalOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FractionalOwnership
        fields = '__all__'
        
        
class TokenTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenTransaction
        fields = '__all__'