
import requests

from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt    
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    BlockchainWalletSerializer,
    KYCVerificationSerializer,
    InvestorProfileSerializer
)

from allauth.account.utils import send_email_confirmation
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress as allauthEmailAddress
from allauth.account.utils import complete_signup
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.providers.google.provider import GoogleProvider

from .models import CustomUser, UserProfile, BlockchainWallet, KYCVerification, InvestorProfile

# Create your views here.
User = get_user_model()



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #email, created = allauthEmailAddress(user = )
        self.perform_create(serializer)
        send_email_confirmation(request, serializer.instance)
        return Response(serializer.data, status=201)
    

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




@login_required
def google_login_callback(request):
    # Get the user from the request
    user = request.user

    # Check if the user is authenticated
    if user.is_authenticated:
        # Get the user's social account (Google)
        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            token = SocialToken.objects.get(account=social_account)

            if token:
                # Token is valid, proceed with login
                # You can also check if the token is expired and refresh it if needed
                #token.token = RefreshToken(token.token)
                #token.save()
                refresh_token = RefreshToken.for_user(user)
                access_token = AccessToken.for_user(user)
                return Response({
                    'refresh': str(refresh_token),
                    'access': str(access_token),
                    'user': {
                        'email': user.email,
                        'id': user.id
                    }
                }, status=200)
                
            # Do something with the token if needed
        except SocialAccount.DoesNotExist:
            return Response({'error': 'Social account not found'}, status=404)
        
        return Response({'message': 'Login successful', 'user': user.email}, status=200)
    
    return Response({'error': 'User not authenticated'}, status=401)

@csrf_exempt
@api_view(["POST"])
def google_signup_login(request):
    """
    Handles Google OAuth signup/login for Next.js frontend.
    """
    token = request.data.get("token")
    if not token:
        return Response({"error": "Google token is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the token with Google
    google_response = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}")
    if google_response.status_code != 200:
        return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

    google_data = google_response.json()
    email = google_data.get("email")
    if not email:
        return Response({"error": "Google token did not return an email"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user already exists
    try:
        social_account = SocialAccount.objects.get(uid=google_data["sub"], provider=GoogleProvider.id)
        user = social_account.user
    except SocialAccount.DoesNotExist:
        # Create a new user if it doesn't exist
        user = User.objects.create(
            username=email,
            email=email,
            first_name=google_data.get("given_name", ""),
            last_name=google_data.get("family_name", ""),
        )
        user.set_unusable_password()
        user.save()

        # Link the social account
        social_account = SocialAccount.objects.create(
            user=user,
            uid=google_data["sub"],
            provider=GoogleProvider.id,
            extra_data=google_data,
        )

    # Log the user in
    login(request, user)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        "refresh": str(refresh),
        "access": str(access),
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }, status=status.HTTP_200_OK)


@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        # Get the user's email from the request
        email = request.POST.get('email')
        
        # Check if the user exists
        try:
            user = CustomUser.objects.get(email=email)
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh_token),
                'access': str(access_token),
                'user': {
                    'email': user.email,
                    'id': user.id
                }
            }, status=200)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    return Response({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def web3_login(request):
    if request.method == 'POST':
        # Get the user's address from the request
        address = request.POST.get('address')
        
        # Check if the user exists
        try:
            user = CustomUser.objects.get(wallet_address=address)
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh_token),
                'access': str(access_token),
                'user': {
                    'address': user.wallet_address,
                    'id': user.id
                }
            }, status=200)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    return Response({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def web3_login_callback(request):
    if request.method == 'POST':
        # Get the user's address from the request
        address = request.POST.get('address')
        
        # Check if the user exists
        try:
            user = CustomUser.objects.get(wallet_address=address)
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh_token),
                'access': str(access_token),
                'user': {
                    'address': user.wallet_address,
                    'id': user.id
                }
            }, status=200)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    
    return Response({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        print("Token", token)
        # Validate the token with Google
        # You can use the Google API to validate the token here
        # For example, using requests library:
        response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token}')
        print("RESPONSE", response)
        
        # If the token is valid, return success
        return Response({'message': 'Token is valid'}, status=200)
    
    return Response({'error': 'Invalid request method'}, status=400)