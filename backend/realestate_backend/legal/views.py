from django.shortcuts import render
from rest_framework import viewsets
from .models import RegulatoryCheck, TaxRecord, LegalDocument, ComplianceRule
from .serializers import (
    RegulatoryCheckSerializer,
    TaxRecordSerializer,
    LegalDocumentSerializer,
    ComplianceRuleSerializer,
)

# Create your views here.


class RegulatoryCheckViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing RegulatoryCheck objects.
    """
    queryset = RegulatoryCheck.objects.all()
    serializer_class = RegulatoryCheckSerializer
    filterset_fields = ['user', 'status', 'check_type']
    search_fields = ['external_reference', 'verification_hash']


class TaxRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing TaxRecord objects.
    """
    queryset = TaxRecord.objects.all()
    serializer_class = TaxRecordSerializer
    filterset_fields = ['user', 'record_type', 'jurisdiction', 'tax_year']
    search_fields = ['filing_reference']


class LegalDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LegalDocument objects.
    """
    queryset = LegalDocument.objects.all()
    serializer_class = LegalDocumentSerializer
    filterset_fields = ['document_type', 'signature_status']
    search_fields = ['title', 'hash_sha256']


class ComplianceRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing ComplianceRule objects.
    """
    queryset = ComplianceRule.objects.all()
    serializer_class = ComplianceRuleSerializer
    filterset_fields = ['scope', 'enforcement_level', 'jurisdiction', 'is_active']
    search_fields = ['rule_id', 'name', 'description']