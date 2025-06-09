from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegulatoryCheckViewSet,
    TaxRecordViewSet,
    LegalDocumentViewSet,
    ComplianceRuleViewSet,
)

router = DefaultRouter()

router.register(r'regulatory_checks', RegulatoryCheckViewSet, basename='regulatorycheck')
router.register(r'tax_records', TaxRecordViewSet, basename='taxrecord')
router.register(r'legal_documents', LegalDocumentViewSet, basename='legaldocument')
router.register(r'compliance_rules', ComplianceRuleViewSet, basename='compliancerule')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
