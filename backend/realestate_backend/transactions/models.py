from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Investment(models.Model):
    INVESTMENT_TYPES = (
        ('DIRECT', 'Direct Purchase'),
        ('FRACTIONAL', 'Fractional Ownership'),
        ('FUND', 'Investment Fund')
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('LIQUIDATED', 'Liquidated'),
        ('DEFAULTED', 'Defaulted')
    )

    # Core Relationships
    investor = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='investments')
    asset = models.ForeignKey('tokenization.TokenizedAsset', on_delete=models.PROTECT, related_name='investments')
    
    # Investment Terms
    investment_type = models.CharField(max_length=10, choices=INVESTMENT_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)  # USD
    token_amount = models.DecimalField(max_digits=28, decimal_places=18)
    entry_price = models.DecimalField(max_digits=12, decimal_places=2)  # USD per token
    
    # Status Tracking
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    investment_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)
    exit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Metadata
    contract_hash = models.CharField(max_length=66, blank=True)  # Link to smart contract
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['investor', 'status']),
            models.Index(fields=['asset', 'investment_date']),
        ]

    def __str__(self):
        return f"{self.investor.user.email}'s {self.get_investment_type_display()} in {self.asset.property.title}"
    
    
class DividendPayout(models.Model):
    # Core Relationships
    investment = models.ForeignKey('Investment', on_delete=models.PROTECT, related_name='dividends')
    asset = models.ForeignKey('tokenization.TokenizedAsset', on_delete=models.PROTECT)
    
    # Payout Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # USD
    token_amount = models.DecimalField(max_digits=28, decimal_places=18, null=True, blank=True)
    payout_date = models.DateTimeField()
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Transaction Links
    blockchain_tx = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    is_reinvested = models.BooleanField(default=False)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-payout_date']
        unique_together = [['investment', 'period_start', 'period_end']]

    def __str__(self):
        return f"Dividend for {self.investment}: {self.amount} USD ({self.period_start} to {self.period_end})"
    
    
class Transaction(models.Model):
    TX_TYPES = (
        ('INVESTMENT', 'Investment'),
        ('DIVIDEND', 'Dividend'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TOKEN_TRANSFER', 'Token Transfer'),
        ('ESCROW', 'Escrow Settlement')
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed')
    )

    # Core Fields
    transaction_type = models.CharField(max_length=15, choices=TX_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Parties
    from_user = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='outgoing_transactions', null=True, blank=True)
    to_user = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='incoming_transactions', null=True, blank=True)
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # References
    reference_id = models.CharField(max_length=100, blank=True)  # External ID
    related_asset = models.ForeignKey('tokenization.TokenizedAsset', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Blockchain Data
    blockchain_tx_hash = models.CharField(max_length=66, blank=True)
    blockchain_network = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-initiated_at']
        indexes = [
            models.Index(fields=['from_user', 'status']),
            models.Index(fields=['to_user', 'transaction_type']),
        ]

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} {self.currency} ({self.get_status_display()})"
    
    
class Escrow(models.Model):
    ESCROW_TYPES = (
        ('PURCHASE', 'Property Purchase'),
        ('DIVIDEND', 'Dividend Distribution'),
        ('DISPUTE', 'Dispute Resolution')
    )
    
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('RELEASED', 'Released'),
        ('REFUNDED', 'Refunded'),
        ('DISPUTED', 'In Dispute')
    )

    # Core Configuration
    escrow_type = models.CharField(max_length=10, choices=ESCROW_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Parties
    depositor = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='escrow_deposits')
    beneficiary = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='escrow_benefits', null=True, blank=True)
    
    # Terms
    release_conditions = models.TextField()
    release_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # References
    related_transaction = models.OneToOneField('Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    smart_contract_address = models.CharField(max_length=42, blank=True)

    def __str__(self):
        return f"Escrow {self.id}: {self.amount} {self.currency} ({self.get_status_display()})"