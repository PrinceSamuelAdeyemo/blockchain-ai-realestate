from rest_framework import serializers
from .models import Valuation, MarketTrend, PriceHistory, NeighborhoodData


class ValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = '__all__'


class MarketTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketTrend
        fields = '__all__'


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'


class NeighborhoodDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeighborhoodData
        fields = '__all__'