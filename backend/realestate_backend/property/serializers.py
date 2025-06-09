from rest_framework import serializers
from .models import Property, PropertyType, Amenity, PropertyImage, PropertyDocument

class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyType
        fields = '__all__'

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    #property_type = PropertyTypeSerializer(read_only=True)
    #amenities = AmenitySerializer(many=True, read_only=True)
    #images = PropertyImageSerializer(many=True, read_only=True)
    #documents = PropertyDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'