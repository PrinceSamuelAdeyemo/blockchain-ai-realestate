from django.db import models

# Create your models here.
class TokenizedAsset(models.Model):
    TOKEN_STANDARDS = (
        ('ERC20', 'Fungible Token'),
        ('ERC721', 'Non-Fungible Token'),
        ('ERC1400', 'Security Token')
    )
    
    # Property Linkage
    property = models.OneToOneField(
        'property.Property', 
        on_delete=models.PROTECT,
        related_name='tokenized_asset'
    )
    
    # Token Configuration
    token_standard = models.CharField(max_length=10, choices=TOKEN_STANDARDS)
    token_symbol = models.CharField(max_length=5)  # e.g. "REPTK"
    token_name = models.CharField(max_length=100)  # e.g. "Sunset Villa Tokens"
    total_supply = models.DecimalField(max_digits=28, decimal_places=18)  # To handle crypto decimals
    initial_price = models.DecimalField(max_digits=12, decimal_places=2)  # USD per token
    
    # Blockchain Integration
    contract_address = models.CharField(max_length=42)  # 0x...
    deployer_address = models.CharField(max_length=42)
    deployment_tx_hash = models.CharField(max_length=66)
    deployment_block = models.PositiveBigIntegerField()
    
    # Token Economics
    is_tradable = models.BooleanField(default=False)
    dividend_period = models.CharField(
        max_length=10,
        choices=(('MONTHLY', 'Monthly'), ('QUARTERLY', 'Quarterly')),
        default='QUARTERLY'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class TokenOwnership(models.Model):
    # Ownership Relationships
    owner = models.ForeignKey(
        'core.UserProfile',
        on_delete=models.CASCADE,
        related_name='token_holdings'
    )
    asset = models.ForeignKey(
        TokenizedAsset,
        on_delete=models.CASCADE,
        related_name='ownership_records'
    )
    
    # Balance Tracking
    balance = models.DecimalField(max_digits=28, decimal_places=18)
    locked_balance = models.DecimalField(
        max_digits=28, 
        decimal_places=18,
        default=0
    )  # For vesting periods
    
    # Verification Status
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    # Blockchain Sync
    last_sync_block = models.PositiveBigIntegerField()
    wallet_address = models.CharField(max_length=42)  # Owner's wallet
    
    class Meta:
        unique_together = [['owner', 'asset']]
    
    def __str__(self):
        return f"{self.owner.user.email} - {self.asset.token_symbol}"
    
    
class FractionalOwnership(models.Model):
    # Core Relationships
    token_ownership = models.OneToOneField(
        TokenOwnership,
        on_delete=models.CASCADE,
        related_name='fractional_details'
    )
    
    # Legal Attributes
    ownership_percentage = models.DecimalField(max_digits=7, decimal_places=4)  # e.g. 12.3456%
    acquisition_date = models.DateTimeField()
    acquisition_price = models.DecimalField(max_digits=12, decimal_places=2)  # USD paid
    
    # Governance
    voting_power = models.DecimalField(max_digits=7, decimal_places=4)  # May differ from ownership %
    has_voting_rights = models.BooleanField(default=True)
    
    # Document Links
    ownership_agreement = models.FileField(upload_to='ownership_agreements/')
    agreement_hash = models.CharField(max_length=64)  # SHA-256 of document
    
    def __str__(self):
        return f"{self.token_ownership.owner} - {self.ownership_percentage}%"
    
    
class TokenTransaction(models.Model):
    TX_TYPES = (
        ('MINT', 'Token Minting'),
        ('TRANSFER', 'Peer Transfer'),
        ('DIVIDEND', 'Dividend Payment'),
        ('BURN', 'Token Burn'),
        ('SWAP', 'Exchange Trade')
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed')
    )
    
    # Core References
    asset = models.ForeignKey(
        TokenizedAsset,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    
    # Transaction Metadata
    tx_hash = models.CharField(max_length=66, unique=True)
    tx_type = models.CharField(max_length=10, choices=TX_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    block_number = models.PositiveBigIntegerField()
    timestamp = models.DateTimeField()  # Blockchain timestamp
    
    # Parties Involved
    from_address = models.CharField(max_length=42, null=True, blank=True)
    to_address = models.CharField(max_length=42, null=True, blank=True)
    
    # Value Tracking
    amount = models.DecimalField(max_digits=28, decimal_places=18)
    gas_used = models.DecimalField(max_digits=12, decimal_places=0)  # Wei
    gas_price = models.DecimalField(max_digits=12, decimal_places=0)  # Wei
    
    # Additional Data
    input_data = models.TextField(null=True, blank=True)  # Raw tx input
    event_logs = models.JSONField(null=True, blank=True)  # Parsed event data
    
    class Meta:
        ordering = ['-block_number']
        indexes = [
            models.Index(fields=['tx_hash']),
            models.Index(fields=['from_address']),
            models.Index(fields=['to_address']),
            models.Index(fields=['block_number']),
        ]
    
    def __str__(self):
        return f"{self.get_tx_type_display()} - {self.tx_hash[:10]}..."