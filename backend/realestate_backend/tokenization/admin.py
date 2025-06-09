from django.contrib import admin
from .models import (
    TokenizedAsset,
    TokenOwnership,
    FractionalOwnership,
    TokenTransaction
)
# Register your models here.
admin.site.register([
    TokenizedAsset, 
    TokenOwnership, 
    FractionalOwnership,
    TokenTransaction
])