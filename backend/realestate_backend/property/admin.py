from django.contrib import admin
from . models import (
    Property,
    PropertyType,
    Amenity,
    PropertyImage,
    PropertyDocument
)
# Register your models here.
admin.site.register([
    Property,
    PropertyType,
    Amenity,
    PropertyImage,
    PropertyDocument
])