from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Valuation, MarketTrend, PriceHistory, NeighborhoodData
# Register your models here.
admin.site.register([
    Valuation,
    MarketTrend,
    PriceHistory,
    NeighborhoodData
])