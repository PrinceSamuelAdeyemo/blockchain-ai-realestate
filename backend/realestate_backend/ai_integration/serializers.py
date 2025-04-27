from rest_framework import serializers
from .models import ModelVersion, Prediction, TrainingData, FeatureSet


class ModelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelVersion
        fields = [
            'id', 'model_type', 'version', 'framework', 'storage_path', 'checksum',
            'is_production', 'training_data', 'feature_set', 'hyperparameters',
            'metrics', 'parent_version', 'deployed_at', 'deployed_by', 'created_at'
        ]


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = [
            'id', 'model_version', 'property', 'market', 'input_data', 'output_data',
            'interpreted_result', 'confidence_score', 'prediction_time', 'batch_id',
            'created_at'
        ]


class TrainingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingData
        fields = [
            'id', 'name', 'data_type', 'version', 'storage_location', 'size_gb',
            'record_count', 'date_range_start', 'date_range_end', 'geographic_scope',
            'data_schema', 'parent_version', 'created_at', 'updated_at'
        ]


class FeatureSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureSet
        fields = [
            'id', 'name', 'version', 'features', 'transformations', 'required_data',
            'feature_importance', 'correlation_matrix', 'parent_version',
            'created_at', 'updated_at'
        ]