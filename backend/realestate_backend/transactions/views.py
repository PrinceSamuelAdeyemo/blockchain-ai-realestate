from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Investment,
    DividendPayout,
    Transaction,
    Escrow
)
from .serializers import (
    InvestmentSerializer,
    DividendPayoutSerializer,
    TransactionSerializer,
    EscrowSerializer
)

# Create your views here.

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    
    
class DividendPayoutViewSet(viewsets.ModelViewSet):
    queryset = DividendPayout.objects.all()
    serializer_class = DividendPayoutSerializer
    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
    
class EscrowViewSet(viewsets.ModelViewSet):
    queryset = Escrow.objects.all()
    serializer_class = EscrowSerializer