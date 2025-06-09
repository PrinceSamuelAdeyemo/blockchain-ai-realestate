from django.contrib import admin
from .models import RegulatoryCheck, TaxRecord, LegalDocument, ComplianceRule

# Register your models here.
admin.site.register([
    RegulatoryCheck,
    TaxRecord,
    LegalDocument,
    ComplianceRule,
])