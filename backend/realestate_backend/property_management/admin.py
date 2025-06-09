from django.contrib import admin
from .models import Lease, Tenant, MaintenanceRequest, Inspection
# Register your models here.
admin.site.register([
    Lease,
    Tenant,
    MaintenanceRequest,
    Inspection
    ])
