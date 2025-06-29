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
        fields = "__all__"
        extra_kwargs = {
            "image": {"required": True}
        }

class PropertyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDocument
        fields = "__all__"
        extra_kwargs = {
            "file": {"required": True}
        }

class PropertySerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer(read_only=True)
    property_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PropertyType.objects.all(), source="property_type", write_only=True
    )
    amenities = AmenitySerializer(many=True, read_only=True)
    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(), many=True, source="amenities", write_only=True
    )
    images = PropertyImageSerializer(many=True, read_only=True)
    documents = PropertyDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id", "title", "slug", "address", "city", "state", "country", "postal_code",
            "latitude", "longitude", "property_type", "property_type_id",
            "amenities", "amenity_ids", "total_area", "usable_area", "total_floors", "floor_number",
            "plot_size", "bedrooms", "bathrooms", "year_built", "description",
            "base_value", "price_per_sqm", "rental_price", "current_rent",
            "purchase_type", "is_available_for_rent", "crowdfund_target", "amount_raised",
            "crowdfund_start_date", "blockchain_tx_hash", "status", "is_featured",
            "created_at", "updated_at", "images", "documents"
        ]
        read_only_fields = ["id", "created_at", "updated_at", "images", "documents"]

    def create(self, validated_data):
        amenities = validated_data.pop("amenities", [])
        property_type = validated_data.pop("property_type")
        property_obj = Property.objects.create(property_type=property_type, **validated_data)
        property_obj.amenities.set(amenities)
        return property_obj
    
    def update(self, instance, validated_data):
        amenities = validated_data.pop("amenities", None)
        property_type = validated_data.pop("property_type", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if property_type:
            instance.property_type = property_type
        if amenities is not None:
            instance.amenities.set(amenities)
        instance.save()
        return instance