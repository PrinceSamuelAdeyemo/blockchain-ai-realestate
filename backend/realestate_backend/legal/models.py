from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.
class RegulatoryCheck(models.Model):
    CHECK_TYPES = (
        ('KYC', 'Know Your Customer'),
        ('AML', 'Anti-Money Laundering'),
        ('ACCREDITATION', 'Investor Accreditation'),
        ('JURISDICTION', 'Jurisdictional Compliance')
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('EXEMPT', 'Exempt')
    )

    # Core Relationships
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='regulatory_checks')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Check Details
    check_type = models.CharField(max_length=15, choices=CHECK_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requirement = models.ForeignKey('ComplianceRule', on_delete=models.PROTECT)
    
    # Verification Data
    submitted_data = models.JSONField()  # Structured form data
    documents = models.ManyToManyField('LegalDocument', blank=True)
    external_reference = models.CharField(max_length=100, blank=True)  # ID from 3rd party service
    
    # Blockchain Integration
    verification_hash = models.CharField(max_length=66, blank=True)  # Stored on-chain
    verification_block = models.PositiveBigIntegerField(null=True, blank=True)
    
    # Dates
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [['user', 'check_type', 'requirement']]
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['check_type', 'expires_at']),
        ]

    def __str__(self):
        return f"{self.get_check_type_display()} Check for {self.user.user.email} ({self.get_status_display()})"
    
    
class TaxRecord(models.Model):
    RECORD_TYPES = (
        ('INCOME', 'Rental Income'),
        ('CAPITAL_GAINS', 'Capital Gains'),
        ('WITHHOLDING', 'Tax Withholding'),
        ('FILING', 'Tax Filing')
    )
    
    JURISDICTIONS = (
        ('US', 'United States'),
        ('EU', 'European Union'),
        ('UK', 'United Kingdom'),
        ('SG', 'Singapore')
    )

    # Core Relationships
    user = models.ForeignKey('core.UserProfile', on_delete=models.CASCADE, related_name='tax_records')
    property = models.ForeignKey('property.Property', on_delete=models.SET_NULL, null=True, blank=True)
    investment = models.ForeignKey('transactions.Investment', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Record Details
    record_type = models.CharField(max_length=15, choices=RECORD_TYPES)
    jurisdiction = models.CharField(max_length=5, choices=JURISDICTIONS)
    tax_year = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Document Storage
    forms = models.ManyToManyField('LegalDocument', blank=True)
    calculation_breakdown = models.JSONField()  # Structured tax calculation
    
    # Status
    is_filed = models.BooleanField(default=False)
    filing_reference = models.CharField(max_length=100, blank=True)
    
    # Dates
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'record_type', 'tax_year', 'jurisdiction']]
        ordering = ['-tax_year', 'jurisdiction']

    def __str__(self):
        return f"{self.get_record_type_display()} Tax {self.tax_year} - {self.user.user.email}"
    
    @classmethod
    def calculate_investor_tax(cls, user, year):
        """Automatically calculate tax liability"""
        from decimal import Decimal
        
        investments = Investment.objects.filter(
            investor=user,
            investment_date__year__lte=year
        ).select_related('asset')
        
        dividends = DividendPayout.objects.filter(
            owner=user,
            payout_date__year=year
        )
        
        # Calculate capital gains
        realized_gains = sum(
            inv.exit_price - inv.entry_price 
            for inv in investments 
            if inv.exit_date and inv.exit_date.year == year
        )
        
        # Calculate dividend income
        dividend_income = sum(
            div.amount for div in dividends
        )
        
        # Apply jurisdiction-specific rules
        if user.profile.country == 'US':
            return {
                'capital_gains': realized_gains * Decimal('0.20'),
                'dividend_income': dividend_income * Decimal('0.15'),
                'total_liability': (realized_gains * Decimal('0.20')) + (dividend_income * Decimal('0.15'))
            }
        # Other jurisdictions...
    
    def generate_1099_form(self):
        """Generate IRS Form 1099 for US investors"""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # PDF generation logic
        p.drawString(100, 750, f"FORM 1099 - {self.get_record_type_display()}")
        p.drawString(100, 730, f"Recipient: {self.user.user.get_full_name()}")
        p.drawString(100, 710, f"Amount: ${self.amount}")
        
        if self.property:
            p.drawString(100, 690, f"Property: {self.property.title}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer
    
    
class LegalDocument(models.Model):
    DOCUMENT_TYPES = (
        ('CONTRACT', 'Contract Agreement'),
        ('DISCLOSURE', 'Disclosure Document'),
        ('CERTIFICATE', 'Legal Certificate'),
        ('GOVERNMENT', 'Government Filing'),
        ('TERMS', 'Terms of Service')
    )
    
    SIGNATURE_STATUS = (
        ('UNSIGNED', 'Unsigned'),
        ('PENDING', 'Signature Pending'),
        ('COMPLETE', 'Fully Executed'),
        ('EXPIRED', 'Expired')
    )

    # Core Information
    document_type = models.CharField(max_length=15, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    language = models.CharField(max_length=10, default='en')
    
    # Content Storage
    document_file = models.FileField(upload_to='legal_documents/')
    hash_sha256 = models.CharField(max_length=64)  # Document fingerprint
    template_id = models.CharField(max_length=50, blank=True)  # For template-based docs
    
    # Signatures
    signature_status = models.CharField(max_length=10, choices=SIGNATURE_STATUS, default='UNSIGNED')
    signature_data = models.JSONField(default=dict)  # {signatories: [], timestamps: []}
    blockchain_proof = models.CharField(max_length=66, blank=True)  # Tx hash of notarization
    
    # Relationships
    related_users = models.ManyToManyField('core.UserProfile', blank=True)
    related_properties = models.ManyToManyField('property.Property', blank=True)
    governing_law = models.CharField(max_length=100, blank=True)  # e.g., "California Law"
    
    # Dates
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['title', 'version']]
        indexes = [
            models.Index(fields=['document_type', 'signature_status']),
        ]

    def __str__(self):
        return f"{self.title} v{self.version} ({self.get_document_type_display()})"
    
    def initiate_signing(self, signers):
        """Start electronic signature process"""
        from .integrations.docusign import DocusignClient
        
        client = DocusignClient()
        envelope_id = client.create_envelope(
            document_path=self.document_file.path,
            signers=signers,
            subject=f"Please sign: {self.title}"
        )
        
        self.signature_status = 'PENDING'
        self.signature_data = {
            'envelope_id': envelope_id,
            'signers': signers,
            'sent_at': timezone.now().isoformat()
        }
        self.save()
        
        return envelope_id
    
    def notarize_on_chain(self):
        """Store document proof on blockchain"""
        from web3 import Web3
        from .utils import get_web3_provider
        
        w3 = get_web3_provider()
        contract = w3.eth.contract(
            address=settings.NOTARIZATION_CONTRACT,
            abi=settings.NOTARIZATION_ABI
        )
        
        tx_hash = contract.functions.notarizeDocument(
            Web3.keccak(text=self.hash_sha256),
            int(timezone.now().timestamp())
        ).transact({
            'from': settings.PLATFORM_WALLET
        })
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.blockchain_proof = tx_hash.hex()
        self.save()
        
        return receipt
    
    
class ComplianceRule(models.Model):
    RULE_SCOPES = (
        ('GLOBAL', 'Platform-wide'),
        ('JURISDICTION', 'Jurisdiction-specific'),
        ('ASSET_TYPE', 'Asset-type Specific'),
        ('USER_TYPE', 'User-type Specific')
    )
    
    ENFORCEMENT_LEVELS = (
        ('HARD', 'Hard Requirement'),
        ('SOFT', 'Advisory'),
        ('NOTICE', 'Disclosure Only')
    )

    # Core Identification
    rule_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    scope = models.CharField(max_length=15, choices=RULE_SCOPES)
    enforcement_level = models.CharField(max_length=10, choices=ENFORCEMENT_LEVELS)
    
    # Rule Parameters
    jurisdiction = models.CharField(max_length=100, blank=True)  # ISO country codes
    asset_types = models.ManyToManyField('property.PropertyType', blank=True)
    user_types = models.JSONField(default=list)  # ['INVESTOR', 'PROPERTY_OWNER']
    
    # Rule Logic
    condition = models.JSONField()  # Structured logic for evaluation
    requirements = models.JSONField()  # Required documents/checks
    automated_checks = models.BooleanField(default=False)
    
    # Governance
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    source_regulation = models.CharField(max_length=200, blank=True)  # e.g., "SEC Regulation D"
    
    # Versioning
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    sunset_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rule_id', '-version']
        get_latest_by = 'version'

    def __str__(self):
        return f"{self.rule_id} v{self.version}: {self.name}"
    
    @classmethod
    def handle_regulatory_change(cls, jurisdiction, changeset):
        """Bulk update rules for regulatory changes"""
        from django.db import transaction
        
        with transaction.atomic():
            # Sunset old rules
            cls.objects.filter(
                jurisdiction=jurisdiction,
                is_active=True
            ).update(
                is_active=False,
                sunset_date=timezone.now().date()
            )
            
            # Create new rules
            new_rules = []
            for rule_data in changeset['new_rules']:
                new_rules.append(cls(
                    rule_id=rule_data['id'],
                    name=rule_data['name'],
                    description=rule_data['description'],
                    jurisdiction=jurisdiction,
                    # ... other fields ...
                ))
            
            cls.objects.bulk_create(new_rules)
            
            # Return change summary
            return {
                'sunset_rules': cls.objects.filter(
                    jurisdiction=jurisdiction,
                    sunset_date=timezone.now().date()
                ).count(),
                'new_rules': len(new_rules)
            }
    
    def evaluate_for_user(self, user_profile):
        """Evaluate rule against a specific user"""
        from .utils import RuleEngine
        
        engine = RuleEngine(
            rule_condition=self.condition,
            user_context=user_profile.get_compliance_context()
        )
        
        return {
            'passed': engine.evaluate(),
            'missing_requirements': engine.get_missing_requirements(),
            'required_actions': engine.get_required_actions()
        }
        
    def get_compliance_status(user_id):
        """Get comprehensive compliance status for dashboard"""
        from django.db.models import Count, Q
        
        checks = RegulatoryCheck.objects.filter(
            user_id=user_id
        ).values('check_type').annotate(
            total=Count('id'),
            approved=Count('id', filter=Q(status='APPROVED')),
            pending=Count('id', filter=Q(status='PENDING')),
            expired=Count('id', filter=Q(expires_at__lt=timezone.now()))
        )
        
        outstanding = ComplianceRule.objects.filter(
            Q(jurisdiction='GLOBAL') | Q(jurisdiction=user.profile.country),
            is_active=True
        ).exclude(
            id__in=RegulatoryCheck.objects.filter(
                user_id=user_id,
                status='APPROVED'
            ).values('requirement_id')
        )
        
        return {
            'checks': list(checks),
            'outstanding_rules': outstanding.count(),
            'completion_percentage': (
                checks.approved / checks.total * 100 
                if checks.total > 0 else 100
            )
        }


