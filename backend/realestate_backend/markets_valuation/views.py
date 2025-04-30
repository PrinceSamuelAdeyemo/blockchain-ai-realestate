from django.shortcuts import render
from rest_framework import viewsets
from .models import Valuation, MarketTrend, PriceHistory, NeighborhoodData
from .serializers import (
    ValuationSerializer,
    MarketTrendSerializer,
    PriceHistorySerializer,
    NeighborhoodDataSerializer,
)

# Create your views here.


class ValuationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Valuation objects.
    """
    queryset = Valuation.objects.all()
    serializer_class = ValuationSerializer


class MarketTrendViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing MarketTrend objects.
    """
    queryset = MarketTrend.objects.all()
    serializer_class = MarketTrendSerializer


class PriceHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PriceHistory objects.
    """
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer


class NeighborhoodDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing NeighborhoodData objects.
    """
    queryset = NeighborhoodData.objects.all()
    serializer_class = NeighborhoodDataSerializer