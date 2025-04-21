from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, UserProfile, BlockchainWallet, KYCVerification, InvestorProfile
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    BlockchainWalletSerializer,
    KYCVerificationSerializer,
    InvestorProfileSerializer
)
# Create your views here.


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class BlockchainWalletViewSet(viewsets.ModelViewSet):
    queryset = BlockchainWallet.objects.all()
    serializer_class = BlockchainWalletSerializer
    permission_classes = [IsAuthenticated]

class KYCVerificationViewSet(viewsets.ModelViewSet):
    queryset = KYCVerification.objects.all()
    serializer_class = KYCVerificationSerializer
    permission_classes = [IsAuthenticated]

class InvestorProfileViewSet(viewsets.ModelViewSet):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = [IsAuthenticated]