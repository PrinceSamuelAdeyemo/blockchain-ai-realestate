from rest_framework import serializers
from .models import (
    CustomUser,
    UserProfile,
    BlockchainWallet,
    KYCVerification,
    InvestorProfile
)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'blockchain', 'wallet_address',
            'is_active', 'is_staff', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_type', 'phone_number', 'profile_image',
            'bio', 'is_verified', 'verification_level', 'preferred_currency',
            'language', 'default_wallet', 'created_at', 'last_updated'
        ]


class BlockchainWalletSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField()

    class Meta:
        model = BlockchainWallet
        fields = [
            'id', 'user_profile', 'address', 'wallet_type', 'is_active',
            'is_hardware', 'last_backup', 'network', 'derivation_path',
            'created_at', 'last_used'
        ]


class KYCVerificationSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField()

    class Meta:
        model = KYCVerification
        fields = [
            'id', 'user_profile', 'full_legal_name', 'date_of_birth',
            'nationality', 'tax_id', 'id_type', 'id_number', 'id_front',
            'id_back', 'selfie', 'status', 'verified_by', 'verification_date',
            'rejection_reason', 'verification_hash', 'submitted_at', 'expires_at'
        ]


class InvestorProfileSerializer(serializers.ModelSerializer):
    user_profile = serializers.StringRelatedField()

    class Meta:
        model = InvestorProfile
        fields = [
            'id', 'user_profile', 'risk_tolerance', 'investment_goals',
            'preferred_property_types', 'target_countries', 'target_cities',
            'min_investment', 'max_investment', 'target_roi',
            'preferred_hold_period', 'requires_secondary_market',
            'wants_dividend_reinvestment', 'alert_on_new_properties',
            'last_updated'
        ]