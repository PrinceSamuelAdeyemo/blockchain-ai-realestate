from django.db import models

# Create your models here.
class VotingProposal(models.Model):
    PROPOSAL_TYPES = (
        ('PLATFORM', 'Platform Governance'),
        ('ASSET', 'Asset Management'),
        ('TREASURY', 'Treasury Allocation'),
        ('UPGRADE', 'System Upgrade')
    )
    
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Voting Active'),
        ('PASSED', 'Proposal Passed'),
        ('REJECTED', 'Proposal Rejected'),
        ('IMPLEMENTED', 'Implemented')
    )

    # Core Relationships
    tokenized_asset = models.ForeignKey(
        'TokenizedAsset',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='proposals'
    )
    proposed_by = models.ForeignKey('UserProfile', on_delete=models.PROTECT)

    # Proposal Details
    proposal_type = models.CharField(max_length=10, choices=PROPOSAL_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='DRAFT')
    
    # Voting Parameters
    voting_system = models.CharField(
        max_length=20,
        choices=(('SIMPLE_MAJORITY', '50%+1'), ('SUPER_MAJORITY', '67%'), ('QUORUM', 'Quorum')),
        default='SIMPLE_MAJORITY'
    )
    start_block = models.PositiveBigIntegerField()  # Snapshot block
    end_block = models.PositiveBigIntegerField()
    min_tokens_to_pass = models.DecimalField(max_digits=28, decimal_places=18, null=True, blank=True)
    
    # Execution
    execution_calls = models.JSONField()  # Array of {contract: address, function: name, args: []}
    executed_at = models.DateTimeField(null=True, blank=True)
    execution_tx = models.CharField(max_length=66, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tokenized_asset', 'status']),
            models.Index(fields=['proposal_type', 'end_block']),
        ]

    def __str__(self):
        return f"Proposal: {self.title} ({self.get_status_display()})"
    
    def execute_proposal(self):
        from web3 import Web3
        from .utils import get_web3_provider
        
        if self.status != 'PASSED':
            raise ValueError("Only passed proposals can be executed")
            
        w3 = get_web3_provider()
        tx_hashes = []
        
        for call in self.execution_calls:
            contract = SmartContract.objects.get(address=call['contract'])
            contract_instance = w3.eth.contract(
                address=call['contract'],
                abi=contract.abi.abi_json
            )
            tx_hash = getattr(contract_instance.functions, call['function'])(*call['args']).transact({
                'from': settings.GOVERNANCE_WALLET
            })
            tx_hashes.append(tx_hash.hex())
        
        self.execution_tx = json.dumps(tx_hashes)
        self.status = 'IMPLEMENTED'
        self.executed_at = timezone.now()
        self.save()
    
    
class Vote(models.Model):
    VOTE_CHOICES = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('ABSTAIN', 'Abstain')
    )

    # Core Relationships
    proposal = models.ForeignKey('VotingProposal', on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    
    # Voting Data
    choice = models.CharField(max_length=7, choices=VOTE_CHOICES)
    voting_power = models.DecimalField(max_digits=28, decimal_places=18)  # Based on token balance at snapshot
    voted_at_block = models.PositiveBigIntegerField()
    
    # Verification
    signature = models.CharField(max_length=132)  # EIP-712 signature
    is_delegated = models.BooleanField(default=False)
    delegate = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='delegated_votes')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['proposal', 'voter']]
        indexes = [
            models.Index(fields=['proposal', 'choice']),
        ]

    def __str__(self):
        return f"{self.voter.user.email} voted {self.get_choice_display()} on {self.proposal.title}"
    
    
class GovernanceRule(models.Model):
    RULE_SCOPES = (
        ('GLOBAL', 'Platform-wide'),
        ('ASSET', 'Per Asset'),
        ('USER', 'User-specific')
    )

    # Core Configuration
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    scope = models.CharField(max_length=10, choices=RULE_SCOPES, default='GLOBAL')
    is_active = models.BooleanField(default=True)
    
    # Rule Logic
    condition = models.JSONField()  # Structured logic for rule evaluation
    actions = models.JSONField()  # Actions when condition met
    
    # Governance Link
    created_by_proposal = models.ForeignKey('VotingProposal', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Versioning
    version = models.PositiveIntegerField(default=1)
    previous_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', '-version']
        get_latest_by = 'version'

    def __str__(self):
        return f"Governance Rule: {self.name} v{self.version}"