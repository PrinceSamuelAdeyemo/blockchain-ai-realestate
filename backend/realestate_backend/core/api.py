import os

from django.core.cache import cache
from django.utils.crypto import get_random_string
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from eth_account.messages import encode_defunct
from eth_account import Account

User = get_user_model()

class Web3LoginAPI(APIView):
    authentication_classes = []  # Disable default auth
    permission_classes = []

    def post(self, request):
        signature = request.data.get('signature')
        address = request.data.get('address')
        
        # Authenticate via Web3 backend
        user = authenticate(request, signature=signature, address=address)
        if not user:
            return Response({'error': 'Invalid signature'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        login(request, user)  # Optional: for session auth
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'address': user.username,
                'id': user.id
            }
        })
    


@api_view(["POST"])
def get_nonce(request):
    address = request.data.get("address")
    if not address:
        return Response({"error": "Address is required"}, status=400)

    nonce = get_random_string(24)  # e.g., "Sign this message: abc123..."
    cache.set(f"nonce:{address}", nonce, timeout=300)  # 5 minutes
    return Response({"nonce": nonce})



@api_view(["POST"])
def verify_signature(request):
    frontend_web3 = request.data.get("web3", False)
    address = request.data.get("address")
    signature = request.data.get("signature")
    message = request.data.get("message")

    print("\nMessage", message)
    print("\nSignature", signature)
    print("\n"*5)
    print("\nAddress", address)

    if not address or not signature:
        return Response({"error": "Address and signature are required"}, status=400)

    nonce = cache.get(f"nonce:{address}")
    if not nonce:
        return Response({"error": "Nonce expired or invalid"}, status=400)

    message = encode_defunct(text=nonce)

    print(address, signature, message)
    

    try:
        recovered_address = Account.recover_message(message, signature=signature)
    except Exception as e:
        return Response({"error": f"Signature verification failed: {str(e)}"}, status=400)

    if recovered_address != address:
        print("Recovered address:", recovered_address, "Address:", address)
        return Response({"error": "Signature does not match address"}, status=400)
        

    # ✅ Signature is valid — proceed with login or registration
    # For example:
    # user, created = WalletUser.objects.get_or_create(wallet_address=address)
    # token = generate_jwt_for(user)  # optional
    user, created = User.objects.get_or_create(wallet_address=address)
    if created:
        # Optionally, you can set other fields or perform additional actions
        user.blockchain = "Ethereum"
        user.save()

    # Clear nonce after use
    cache.delete(f"nonce:{address}")

    return Response({
        "success": True,
        "address": recovered_address,
        # "token": token  # Optional JWT or session info
    })
