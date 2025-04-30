from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Property, PropertyType, Amenity, PropertyImage, PropertyDocument
from .serializers import (
    PropertySerializer,
    PropertyTypeSerializer,
    AmenitySerializer,
    PropertyImageSerializer,
    PropertyDocumentSerializer,
)

class PropertyTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PropertyType objects.
    """
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class AmenityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Amenity objects.
    """
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


class PropertyImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PropertyImage objects.
    """
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer


class PropertyDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PropertyDocument objects.
    """
    queryset = PropertyDocument.objects.all()
    serializer_class = PropertyDocumentSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Property objects.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer