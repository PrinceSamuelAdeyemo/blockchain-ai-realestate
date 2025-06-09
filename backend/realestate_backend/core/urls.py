from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import (
    CustomUserViewSet,
    UserProfileViewSet,
    BlockchainWalletViewSet,
    KYCVerificationViewSet,
    InvestorProfileViewSet,
    google_login_callback,
    google_login,
    validate_google_token,
)
from .api import Web3LoginAPI, get_nonce, verify_signature
from .session_api import Web3SessionCreateView, Web3SessionVerifyView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'blockchain-wallets', BlockchainWalletViewSet, basename='blockchainwallet')
router.register(r'kyc-verifFications', KYCVerificationViewSet, basename='kycverification')
router.register(r'investor-profiles', InvestorProfileViewSet, basename='investorprofile')

# Define the URL patterns
urlpatterns = [
    path('api/v1/', include(router.urls)),

    # Sessions
    path('api/web3/sessions/', Web3SessionCreateView.as_view()),
    path('api/web3/sessions/verify/', Web3SessionVerifyView.as_view()),
    path('api/web3/sessions/logout/', include('django.contrib.auth.urls')),

    # AllAuth URLs
    path('accounts/', include('allauth.urls')),
    
    # Web3 Auth API
    path('api/auth/web3/login/', Web3LoginAPI.as_view(), name='web3-login'),
    
    # REST Framework Auth
    path('api/auth/', include('rest_framework.urls')),
    
    path("api/auth/nonce", get_nonce, name="get_nonce"),
    path("api/auth/verify", verify_signature, name="verify_signature"),

    path("api/auth/token", TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path("api/auth/token/refresh", TokenRefreshView.as_view(), name = "token_refresh"),
    path("account/", include("allauth.urls")),
    path("callback/", google_login_callback, name = 'google_login_callback'),
    path("api/google/validate/", validate_google_token, name = 'validate_google_token'),


    # path('api/auth/token/', include('rest_framework_simplejwt.urls')),
]