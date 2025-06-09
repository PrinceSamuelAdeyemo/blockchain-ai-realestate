from django.contrib import admin
from .models import (
    ContractEvent,
    SmartContract,
    GasFeeRecord
)
# Register your models here.
admin.site.register([
    ContractEvent,
    SmartContract,
    GasFeeRecord
])