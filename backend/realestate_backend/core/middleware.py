from django.contrib.sessions.middleware import SessionMiddleware
from django.utils.functional import SimpleLazyObject
from web3 import Web3

class Web3SessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)
        
        # Check for Web3 auth header
        if 'HTTP_X_WEB3_SIGNATURE' in request.META:
            signature = request.META['HTTP_X_WEB3_SIGNATURE']
            address = request.META['HTTP_X_WEB3_ADDRESS']
            
            w3 = Web3()
            message = f"Session Request: {request.path}"
            try:
                recovered = w3.eth.account.recover_message(
                    {'message': message, 'signature': signature}
                )
                if recovered.lower() == address.lower():
                    request.web3_user = SimpleLazyObject(
                        lambda: get_user_model().objects.get(username=address.lower())
                    )
            except:
                pass