from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet,
    UserProfileViewSet,
    BlockchainWalletViewSet,
    KYCVerificationViewSet,
    InvestorProfileViewSet
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'blockchain-wallets', BlockchainWalletViewSet, basename='blockchainwallet')
router.register(r'kyc-verifications', KYCVerificationViewSet, basename='kycverification')
router.register(r'investor-profiles', InvestorProfileViewSet, basename='investorprofile')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]