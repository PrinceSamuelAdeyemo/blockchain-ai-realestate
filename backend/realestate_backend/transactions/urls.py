from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    InvestmentViewSet,
    DividendPayoutViewSet,
    TransactionViewSet,
    EscrowViewSet
)

#from rest_framework.authtoken import views as auth_views
#from django.conf import settings

router = DefaultRouter()
router.register(r'investments', InvestmentViewSet, basename='investment')
router.register(r'dividend-payouts', DividendPayoutViewSet, basename='dividend-payout')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'escrows', EscrowViewSet, basename='escrow')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    #path('api-token-auth/', auth_views.obtain_auth_token, name='api_token_auth'),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api-auth-token/', auth_views.obtain_auth_token, name='api_auth_token'),
]
