from django.db import models
import uuid
from core.models import CustomUser

# Create your models here.
User = CustomUser()
class Property(models.Model):
    PROPERTY_STATUS = (
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('SOLD', 'Sold'),
        ('MAINTENANCE', 'Under Maintenance')
    )
    PROPERTY_PURCHASE_TYPES = (
        ('SINGLE', 'single'),
        ('CROWDFUND', 'crowdfund'),
        ('ANY', 'any')
    )
    
    # Core Identification
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    reference_id = models.UUIDField(default=uuid.uuid4, editable=False, blank = True)
    owners = models.ManyToManyField(User, related_name='properties')  # Many-to-many relationship with users
    #reference_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Internal ID
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    
    # Characteristics
    property_type = models.ForeignKey('PropertyType', on_delete=models.PROTECT)
    amenities = models.ManyToManyField('Amenity', blank=True)
    total_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # sqft/m²
    usable_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # sqft/m²
    total_floors = models.PositiveIntegerField(null=True)  # For buildings
    floor_number = models.PositiveIntegerField(null=True)  # For apartments
    plot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # acres/hectares
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    year_built = models.PositiveIntegerField()
    description = models.TextField()
    
    # Financial
    base_value = models.DecimalField(max_digits=15, decimal_places=2)  # Valuation in USD
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2)  # Price per square meter
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Monthly rent
    current_rent = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    purchase_type = models.CharField(max_length=9, choices=PROPERTY_PURCHASE_TYPES, default='ANY', blank=True, null=True)  # single or crowdfund
    is_available_for_rent = models.BooleanField(default=False)  # For rental properties
    
    # Blockchain related
    blockchain_tx_hash = models.CharField(max_length=66, blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='DRAFT')
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.reference_id} - {self.title}"
    
    
class PropertyType(models.Model):
    CATEGORIES = (
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('INDUSTRIAL', 'Industrial'),
        ('LAND', 'Land')
    )
    
    name = models.CharField(max_length=100)  # e.g., "Apartment", "Office Building"
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For UI icons
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"
    
    
class Amenity(models.Model):
    AMENITY_TYPES = (
        ('BUILDING', 'Building Amenity'),
        ('UNIT', 'Unit Amenity'),
        ('COMMUNITY', 'Community Amenity')
    )
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=AMENITY_TYPES)
    icon = models.CharField(max_length=50, blank=True)  # For UI
    is_standard = models.BooleanField(default=False)  # Common amenities
    
    def __str__(self):
        return self.name
    
    
class PropertyImage(models.Model):
    IMAGE_TYPES = (
        ('MAIN', 'Main Image'),
        ('FLOOR_PLAN', 'Floor Plan'),
        ('INTERIOR', 'Interior View'),
        ('EXTERIOR', 'Exterior View'),
        ('AERIAL', 'Aerial View')
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    caption = models.CharField(max_length=200, blank=True)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='INTERIOR')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # For sorting
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.property.title} - {self.get_image_type_display()}"
    

class PropertyDocument(models.Model):
    DOCUMENT_TYPES = (
        ('DEED', 'Title Deed'),
        ('BLUEPRINT', 'Blueprint'),
        ('SURVEY', 'Survey Report'),
        ('PERMIT', 'Building Permit'),
        ('CERTIFICATE', 'Occupancy Certificate'),
        ('CONTRACT', 'Sales Contract'),
        ('OTHER', 'Other')
    )
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='property_documents/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.property.title} - {self.get_document_type_display()}"
    
