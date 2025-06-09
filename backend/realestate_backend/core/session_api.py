from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from web3 import Web3

class Web3SessionCreateView(APIView):
    def post(self, request):
        signature = request.data.get('signature')
        address = request.data.get('address')
        
        # Verify signature
        w3 = Web3()
        message = "Create Persistent Session"
        try:
            recovered = w3.eth.account.recover_message(
                {'message': message, 'signature': signature}
            )
            if recovered.lower() != address.lower():
                return Response({'error': 'Invalid signature'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'error': 'Signature verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create user
        user = authenticate(request, signature=signature, address=address)
        if not user:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Create Django session
        login(request, user)
        request.session['web3_address'] = address.lower()
        request.session['web3_auth'] = True
        
        return Response({
            'status': 'session_created',
            'sessionid': request.session.session_key,
            'user': {
                'address': address,
                'id': user.id
            }
        })

class Web3SessionVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if hasattr(request, 'web3_user'):
            return Response({'status': 'web3_authenticated'})
        return Response({'status': 'traditional_auth'})