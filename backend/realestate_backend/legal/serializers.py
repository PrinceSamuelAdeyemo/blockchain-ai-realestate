from rest_framework import serializers
from .models import RegulatoryCheck, TaxRecord, LegalDocument, ComplianceRule


class RegulatoryCheckSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.user.email', read_only=True)
    verified_by_email = serializers.EmailField(source='verified_by.email', read_only=True)

    class Meta:
        model = RegulatoryCheck
        fields = [
            'id',
            'user',
            'user_email',
            'verified_by',
            'verified_by_email',
            'check_type',
            'status',
            'requirement',
            'submitted_data',
            'documents',
            'external_reference',
            'verification_hash',
            'verification_block',
            'submitted_at',
            'reviewed_at',
            'expires_at',
        ]
        read_only_fields = ['id', 'submitted_at', 'reviewed_at', 'verification_hash', 'verification_block']


class TaxRecordSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.user.email', read_only=True)

    class Meta:
        model = TaxRecord
        fields = [
            'id',
            'user',
            'user_email',
            'property',
            'investment',
            'record_type',
            'jurisdiction',
            'tax_year',
            'amount',
            'currency',
            'forms',
            'calculation_breakdown',
            'is_filed',
            'filing_reference',
            'period_start',
            'period_end',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = [
            'id',
            'document_type',
            'title',
            'version',
            'language',
            'document_file',
            'hash_sha256',
            'template_id',
            'signature_status',
            'signature_data',
            'blockchain_proof',
            'related_users',
            'related_properties',
            'governing_law',
            'effective_date',
            'expiration_date',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ComplianceRuleSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)

    class Meta:
        model = ComplianceRule
        fields = [
            'id',
            'rule_id',
            'name',
            'description',
            'scope',
            'enforcement_level',
            'jurisdiction',
            'asset_types',
            'user_types',
            'condition',
            'requirements',
            'automated_checks',
            'created_by',
            'created_by_email',
            'source_regulation',
            'version',
            'is_active',
            'effective_date',
            'sunset_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']