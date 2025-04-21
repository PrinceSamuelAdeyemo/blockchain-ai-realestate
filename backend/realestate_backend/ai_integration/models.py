from django.db import models

# Create your models here.
class ModelVersion(models.Model):
    MODEL_TYPES = (
        ('VALUATION', 'Property Valuation'),
        ('PREDICTIVE', 'Market Prediction'),
        ('RECOMMENDER', 'Investment Recommender'),
        ('RISK', 'Risk Assessment')
    )

    FRAMEWORKS = (
        ('TENSORFLOW', 'TensorFlow'),
        ('PYTORCH', 'PyTorch'),
        ('SKLEARN', 'Scikit-learn'),
        ('XGBOOST', 'XGBoost')
    )

    # Core Identification
    model_type = models.CharField(max_length=15, choices=MODEL_TYPES)
    version = models.CharField(max_length=50)  # Semantic versioning
    framework = models.CharField(max_length=10, choices=FRAMEWORKS)
    
    # Model Artifacts
    storage_path = models.CharField(max_length=255)  # S3/GCS path
    checksum = models.CharField(max_length=64)  # SHA-256
    is_production = models.BooleanField(default=False)
    
    # Training Metadata
    training_data = models.ForeignKey('TrainingData', on_delete=models.PROTECT)
    feature_set = models.ForeignKey('FeatureSet', on_delete=models.PROTECT)
    hyperparameters = models.JSONField()
    metrics = models.JSONField()  # {'accuracy': 0.95, 'precision': 0.93, ...}
    
    # Version Control
    parent_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Deployment
    deployed_at = models.DateTimeField(null=True, blank=True)
    deployed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['model_type', 'version']]
        ordering = ['model_type', '-deployed_at']

    def __str__(self):
        return f"{self.get_model_type_display()} Model v{self.version}"
    
    def deploy_to_production(self):
        from django.db import transaction
        from .tasks import load_model_into_service
        
        with transaction.atomic():
            # Mark previous production model as inactive
            ModelVersion.objects.filter(
                model_type=self.model_type,
                is_production=True
            ).update(is_production=False)
            
            # Actate new model
            self.is_production = True
            self.deployed_at = timezone.now()
            self.save()
            
            # Async load into prediction service
            load_model_into_service.delay(self.id)
    
    
class Prediction(models.Model):
    # Core Relationships
    model_version = models.ForeignKey('ModelVersion', on_delete=models.PROTECT)
    property = models.ForeignKey('Property', on_delete=models.CASCADE, null=True, blank=True)
    market = models.ForeignKey('MarketTrend', on_delete=models.CASCADE, null=True, blank=True)
    
    # Prediction Data
    input_data = models.JSONField()  # Features used
    output_data = models.JSONField()  # Raw model output
    interpreted_result = models.TextField()  # Human-readable explanation
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100%
    
    # Execution Context
    prediction_time = models.DecimalField(max_digits=10, decimal_places=4)  # Seconds
    batch_id = models.CharField(max_length=36, blank=True)  # For batch predictions
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['model_version', 'created_at']),
            models.Index(fields=['property', 'model_version']),
        ]

    def __str__(self):
        target = self.property.title if self.property else self.market.name
        return f"Prediction for {target} by {self.model_version}"
    
    
class TrainingData(models.Model):
    DATA_TYPES = (
        ('STRUCTURED', 'Structured Data'),
        ('IMAGES', 'Image Data'),
        ('TEXT', 'Natural Language'),
        ('TIME_SERIES', 'Time Series')
    )

    # Core Identification
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    version = models.CharField(max_length=50)
    
    # Storage Details
    storage_location = models.CharField(max_length=255)
    size_gb = models.DecimalField(max_digits=10, decimal_places=2)
    record_count = models.PositiveIntegerField()
    
    # Data Characteristics
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    geographic_scope = models.JSONField()  # {'countries': [], 'cities': []}
    data_schema = models.JSONField()  # Field definitions
    
    # Version Control
    parent_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['name', 'version']]
        verbose_name_plural = "Training Data"

    def __str__(self):
        return f"{self.name} v{self.version} ({self.get_data_type_display()})"
    
    
class FeatureSet(models.Model):
    # Core Identification
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    
    # Feature Definitions
    features = models.JSONField()  # List of {name: str, type: str, source: str, description: str}
    transformations = models.JSONField()  # Pipeline steps
    required_data = models.ManyToManyField('TrainingData')
    
    # Performance
    feature_importance = models.JSONField(null=True, blank=True)  # From model analysis
    correlation_matrix = models.JSONField(null=True, blank=True)
    
    # Version Control
    parent_version = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['name', 'version']]

    def __str__(self):
        return f"Feature Set: {self.name} v{self.version}"
    
    def plot_feature_importance(self):
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64
        
        features = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        plt.figure(figsize=(10, 6))
        plt.barh([f[0] for f in features], [f[1] for f in features])
        plt.title('Top 10 Important Features')
        plt.tight_layout()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        
        return base64.b64encode(buffer.getvalue()).decode('utf-8')