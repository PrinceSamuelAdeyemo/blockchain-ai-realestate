from django.contrib import admin
from .models import (
    Investment, 
    DividendPayout,
    Transaction,
    Escrow
)

# Register your models here.
admin.site.register([
    Investment,
    DividendPayout,
    Transaction,
    Escrow
])