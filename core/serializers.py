from rest_framework import serializers
from django.contrib.auth import authenticate
from utilities.jwt_handler import get_tokens_for_user
from django.core.validators import RegexValidator
from .models import Location, CarDetails




class AdminLoginSerializer(serializers.Serializer):

    mobile_number_regex = RegexValidator(
        r"^\+?1?\d{8,15}$", "Only integers are allowed"
        r"^(91|\+91)?-?[6789]\d{9}$",
        "Only valid format are allowed",
    )
    phone = serializers.CharField(
        required=True,
        max_length=16,
        validators=[
            mobile_number_regex,
        ],
    )
    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True,
        error_messages={
            "blank": "Please enter your password.",
        },
    )

    def validate(self, attrs):
        credentials = {
            "phone": attrs.get("phone"),
            "password": attrs.get("password"),
        }
        if not all(credentials.values()):
            message = "Must include phone and password"
            raise serializers.ValidationError(message)
        user = authenticate(**credentials)
        if not user:
            message = "Unable to sign in with provided credentials"
            raise serializers.ValidationError(message)
        if not user.is_active:
            message = "User account is not active"
            raise serializers.ValidationError(message)
        
        tokens = get_tokens_for_user(user)
        user.is_active == True
        user.save()

        return {
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
            "id": user.id,
        }


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class AvailableCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarDetails
        fields = "__all__"