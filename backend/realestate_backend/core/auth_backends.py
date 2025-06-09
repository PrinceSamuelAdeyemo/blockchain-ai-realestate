# myapp/auth_backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from web3 import Web3


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class Web3Backend:
    def authenticate(self, request, signature=None, address=None):
        if not signature or not address:
            return None

        # 1. Verify signature
        w3 = Web3()
        message = "Login to RealEstatePlatform"
        try:
            recovered = w3.eth.account.recover_message(
                {'message': message, 'signature': signature}
            )
            if recovered.lower() != address.lower():
                return None
        except:
            return None

        # 2. Get or create user (compatible with AllAuth)
        user, created = User.objects.get_or_create(username=address.lower())
        if created:
            user.set_unusable_password()  # Web3 users don't need passwords
            user.save()
            user_username(user, address.lower())  # AllAuth compatibility
        
        return user

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
