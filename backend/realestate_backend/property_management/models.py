from django.db import models
import uuid

# Create your models here.
class Lease(models.Model):
    LEASE_TYPES = (
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('SHORT_TERM', 'Short Term')
    )
    
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('TERMINATED', 'Terminated')
    )

    # Core Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Core Relationships
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey('Tenant', on_delete=models.PROTECT, related_name='leases')
    
    # Lease Terms
    lease_type = models.CharField(max_length=15, choices=LEASE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment Details
    payment_due_day = models.PositiveSmallIntegerField(default=1)  # Day of month
    late_fee = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    
    # Status Tracking
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    is_auto_renew = models.BooleanField(default=False)
    
    # Digital Integration
    document = models.FileField(upload_to='lease_agreements/')
    smart_contract = models.ForeignKey('smartcontract.SmartContract', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['property', 'status']),
            models.Index(fields=['tenant', 'end_date']),
        ]

    def __str__(self):
        return f"Lease #{self.id} - {self.property.title}"
    
    
class Tenant(models.Model):
    # Core Relationships
    user_profile = models.OneToOneField(
        'core.UserProfile',
        on_delete=models.CASCADE,
        related_name='tenant_profile',
        null=True,
        blank=True
    )

    # Core Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Contact Information
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=150, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    
    # Rental History
    previous_address = models.TextField(blank=True)
    employer = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    # Verification
    credit_score = models.PositiveSmallIntegerField(null=True, blank=True)
    background_check = models.FileField(upload_to='tenant_checks/', blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Preferences
    preferred_communication = models.CharField(
        max_length=10,
        choices=(('EMAIL', 'Email'), ('SMS', 'Text'), ('CALL', 'Phone Call')),
        default='EMAIL'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tenant: {self.full_name}"
    
    
class MaintenanceRequest(models.Model):
    PRIORITY_LEVELS = (
        ('URGENT', 'Urgent (24h)'),
        ('HIGH', 'High (72h)'),
        ('MEDIUM', 'Medium (1 week)'),
        ('LOW', 'Low (1 month)')
    )
    
    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('DEFERRED', 'Deferred')
    )

    # Core Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Core Relationships
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, related_name='maintenance_requests')
    submitted_by = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='submitted_requests')
    assigned_to = models.ForeignKey('core.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    
    # Request Details
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='MEDIUM')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='SUBMITTED')
    
    # Location Specifics
    area = models.CharField(max_length=100, blank=True)  # e.g., "Kitchen", "Bathroom 2"
    
    # Scheduling
    preferred_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    
    # Media
    before_photos = models.ManyToManyField('property.PropertyImage', blank=True, related_name='maintenance_before')
    after_photos = models.ManyToManyField('property.PropertyImage', blank=True, related_name='maintenance_after')
    
    # Cost Tracking
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'status']
        indexes = [
            models.Index(fields=['property', 'status']),
            models.Index(fields=['assigned_to', 'priority']),
        ]

    def __str__(self):
        return f"Maintenance #{self.id}: {self.title}"
    
    
class Inspection(models.Model):
    INSPECTION_TYPES = (
        ('MOVE_IN', 'Move-In'),
        ('MOVE_OUT', 'Move-Out'),
        ('ROUTINE', 'Routine'),
        ('SPECIAL', 'Special')
    )

    # Core Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Core Relationships
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, related_name='inspections')
    conducted_by = models.ForeignKey('core.UserProfile', on_delete=models.PROTECT, related_name='conducted_inspections')
    
    # Inspection Details
    inspection_type = models.CharField(max_length=10, choices=INSPECTION_TYPES)
    inspection_date = models.DateTimeField()
    next_inspection_date = models.DateTimeField(null=True, blank=True)
    
    # Findings
    summary = models.TextField(blank=True)
    checklist = models.JSONField()  # Structured checklist data
    condition_rating = models.PositiveSmallIntegerField(  # 1-100 scale
        help_text="Overall property condition score",
        null=True,
        blank=True
    )
    
    # Media Documentation
    photos = models.ManyToManyField('property.PropertyImage', blank=True)
    report_document = models.FileField(upload_to='inspection_reports/', blank=True)
    
    # Follow-up
    requires_followup = models.BooleanField(default=False)
    followup_notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-inspection_date']
        get_latest_by = 'inspection_date'

    def __str__(self):
        return f"{self.get_inspection_type_display()} Inspection - {self.property.title}"