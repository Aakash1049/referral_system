from rest_framework import serializers
from .models import User
from django.utils.crypto import get_random_string  # Import this method


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'mobile', 'city', 'referral_code', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_referral_code(self, value):
        """ Validate the referral code during registration. """
        if value:
            # Check if the referral code is valid (exists in the system)
            referrer = User.objects.filter(referral_code=value).first()
            if not referrer:
                raise serializers.ValidationError("Invalid referral code.")
        return value

    def create(self, validated_data):
        # Extract the referral code (if any) from the validated data
        referral_code = validated_data.pop('referral_code', None)
        
        # Find the referrer if referral code exists
        referrer = User.objects.filter(referral_code=referral_code).first() if referral_code else None
        
        # Generate a random referral code for the new user
        referral_code = get_random_string(length=10)  # Generate a random referral code
        
        # Create the user and set the referral code
        user = User.objects.create_user(**validated_data, referral_code=referral_code)
        
        # Assign the referrer if exists
        if referrer:
            user.referrer = referrer
        
        # Save the user instance
        user.save()
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']
