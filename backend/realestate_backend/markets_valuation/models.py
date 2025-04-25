from django.db import models

# Create your models here.
class Valuation(models.Model):
    VALUATION_TYPES = (
        ('AUTOMATED', 'Automated Valuation Model'),
        ('MANUAL', 'Appraiser Valuation'),
        ('HYBRID', 'AI-Assisted')
    )

    # Core Relationships
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, related_name='valuations')
    model_version = models.ForeignKey('ai_integration.ModelVersion', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Valuation Data
    valuation_type = models.CharField(max_length=10, choices=VALUATION_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 0-100%
    valuation_date = models.DateTimeField(auto_now_add=True)
    effective_date = models.DateField()  # Date the valuation applies to
    
    # Market Context
    market_conditions = models.JSONField()  # Stores key metrics snapshot
    comparable_properties = models.ManyToManyField('property.Property', blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ['-valuation_date']
        get_latest_by = 'valuation_date'

    def __str__(self):
        return f"{self.property.title} - {self.value} USD ({self.get_valuation_type_display()})"
    
    
class MarketTrend(models.Model):
    TREND_TYPES = (
        ('PRICE', 'Price Trend'),
        ('DEMAND', 'Demand Trend'),
        ('RENT', 'Rental Trend'),
        ('MACRO', 'Macroeconomic')
    )

    # Geographic Scope
    region_type = models.CharField(max_length=20)  # country/state/city/neighborhood
    region_id = models.CharField(max_length=100)  # ISO code or custom ID
    
    # Trend Data
    trend_type = models.CharField(max_length=10, choices=TREND_TYPES)
    trend_data = models.JSONField()  # {dates: [], values: []}
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    change_30d = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    change_90d = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=100)
    next_update = models.DateTimeField()

    class Meta:
        unique_together = [['region_type', 'region_id', 'trend_type']]
        indexes = [
            models.Index(fields=['region_type', 'trend_type']),
        ]

    def __str__(self):
        return f"{self.get_trend_type_display()} for {self.region_type} {self.region_id}"
    
    
class PriceHistory(models.Model):
    # Core Relationships
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, related_name='price_history')
    
    # Price Data
    date_recorded = models.DateField()
    value = models.DecimalField(max_digits=15, decimal_places=2)
    value_per_sqft = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Context
    source = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, blank=True)  # e.g., "Listing", "Assessment"
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Price Histories"
        ordering = ['property', '-date_recorded']
        unique_together = [['property', 'date_recorded']]

    def __str__(self):
        return f"{self.property.title} - {self.value} USD on {self.date_recorded}"
    
    
class NeighborhoodData(models.Model):
    # Geographic Identification
    neighborhood_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    geo_boundary = models.JSONField()  # GeoJSON polygon
    
    # Key Metrics
    walk_score = models.PositiveSmallIntegerField(null=True, blank=True)
    transit_score = models.PositiveSmallIntegerField(null=True, blank=True)
    safety_index = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    school_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    # Demographic Data
    demographics = models.JSONField(null=True, blank=True)
    amenities = models.JSONField(null=True, blank=True)  # Nearby amenities
    
    # Update Info
    last_updated = models.DateTimeField(auto_now=True)
    data_source = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Neighborhood Data"
        indexes = [
            models.Index(fields=['city', 'country']),
        ]

    def __str__(self):
        return f"{self.name}, {self.city} (Neighborhood Data)"