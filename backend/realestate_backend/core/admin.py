from django.contrib import admin
from .models import CustomUser, UserProfile, BlockchainWallet, KYCVerification, InvestorProfile
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.site_header = "Real Estate Core Admin"
admin.site.site_title = "Real Estate Core Admin Portal"
admin.site.index_title = "Welcome to the Real Estate Core Admin Portal"
admin.site.register([
    # Add your models here
    CustomUser,
    UserProfile,
    BlockchainWallet,
    KYCVerification,
    InvestorProfile
])
