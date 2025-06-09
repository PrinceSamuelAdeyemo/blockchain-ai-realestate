import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin 
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email = None, phone_number = None, wallet_address = None, blockchain = None, password=None, **extra_fields):
        if not email and not password:
            raise ValueError('The given email and password must be set')
        
        #if email:
        email = self.normalize_email(email)
        #extra_fields["email"] = email
        user = self.model(email=email, **extra_fields)
            
        if wallet_address and blockchain:
            #user = self.model(wallet_address=wallet_address, **extra_fields)
            user.wallet_address = wallet_address
            user.blockchain = blockchain
            
        if phone_number:
            user.phone_number = phone_number
            
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email = email, password = password, **extra_fields)
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)#, blank=True, null=True)
    blockchain = models.CharField(max_length=15, blank=True, null=True)
    wallet_address = models.CharField(max_length=42, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or f"User {self.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['wallet_address', 'blockchain', 'email'], name='unique_blockchain_wallet_address_email')
        ]


class Web3Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    address = models.CharField(max_length=42)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    
    class Meta:
        unique_together = [('user', 'session_key')]
        

class UserProfile(models.Model):
    USER_TYPES = (
        ('INVESTOR', 'Investor'),
        ('PROPERTY_OWNER', 'Property Owner'),
        ('ADMIN', 'Admin')
    )
    
    # Core Linkage
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # User Metadata
    user_type = models.CharField(max_length=15, choices=USER_TYPES)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    bio = models.TextField(blank=True)
    
    # Verification Status
    is_verified = models.BooleanField(default=False)
    verification_level = models.PositiveSmallIntegerField(default=0)  # Tiered KYC
    
    # Financial Preferences
    preferred_currency = models.CharField(max_length=3, default='USD')
    language = models.CharField(max_length=10, default='en')
    
    # Blockchain Integration
    default_wallet = models.ForeignKey(
        'BlockchainWallet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
    
    
class BlockchainWallet(models.Model):
    WALLET_TYPES = (
        ('EOA', 'Externally Owned Account'),
        ('CONTRACT', 'Smart Contract Wallet')
    )
    
    # Ownership
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='wallets'
    )
    
    # Wallet Configuration
    address = models.CharField(max_length=42, unique=True)
    wallet_type = models.CharField(max_length=8, choices=WALLET_TYPES)
    is_active = models.BooleanField(default=True)
    
    # Security
    is_hardware = models.BooleanField(default=False)
    last_backup = models.DateTimeField(null=True, blank=True)
    
    # Blockchain Data
    network = models.CharField(max_length=20, default='Ethereum')
    derivation_path = models.CharField(max_length=50, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user_profile', 'address']]
    
    def __str__(self):
        return f"{self.user_profile.user.email}'s Wallet: {self.address[:6]}...{self.address[-4:]}"
    
    
class KYCVerification(models.Model):
    VERIFICATION_STATUS = (
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Verified'),
        ('REJECTED', 'Rejected'),
        ('EXPIRED', 'Expired')
    )
    
    # User Link
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='kyc'
    )
    
    # Personal Details
    full_legal_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Document Verification
    id_type = models.CharField(max_length=20)  # passport, driver's license
    id_number = models.CharField(max_length=50)
    id_front = models.FileField(upload_to='kyc_documents/')
    id_back = models.FileField(upload_to='kyc_documents/', blank=True)
    selfie = models.ImageField(upload_to='kyc_selfies/')
    
    # Verification Metadata
    status = models.CharField(max_length=10, choices=VERIFICATION_STATUS, default='PENDING')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Blockchain Integration
    verification_hash = models.CharField(max_length=66, blank=True)  # Stored on-chain
    
    # Dates
    submitted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # Typically 1 year

    def __str__(self):
        return f"KYC for {self.user_profile.user.email} ({self.get_status_display()})"
    
    
class InvestorProfile(models.Model):
    RISK_LEVELS = (
        ('LOW', 'Low Risk'),
        ('MODERATE', 'Moderate'),
        ('HIGH', 'High Risk')
    )
    
    # Core Link
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='investor_profile'
    )
    
    # Investment Strategy
    risk_tolerance = models.CharField(max_length=10, choices=RISK_LEVELS)
    investment_goals = models.TextField(blank=True)
    preferred_property_types = models.ManyToManyField(
        'property.PropertyType',
        blank=True
    )
    
    # Geographic Preferences
    target_countries = models.JSONField(default=list)  # List of country codes
    target_cities = models.JSONField(default=list)  # List of city names
    
    # Financial Parameters
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, default=1000)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    target_roi = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 7.50%
    
    # Liquidity Preferences
    preferred_hold_period = models.PositiveSmallIntegerField(  # In months
        default=24,
        help_text="Preferred investment duration in months"
    )
    requires_secondary_market = models.BooleanField(default=True)
    
    # Notification Settings
    wants_dividend_reinvestment = models.BooleanField(default=False)
    alert_on_new_properties = models.BooleanField(default=True)
    
    # Dates
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Investment Profile for {self.user_profile.user.email}"
    

