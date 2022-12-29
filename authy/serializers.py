from rest_framework import serializers
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator
from .models import CustomUser
from core.models import CarDetails, RentCar, Location
import pytz

utc = pytz.UTC



class UserRegisterSerializer(serializers.Serializer):
    mobile_number_regex = RegexValidator(
        r"^\+?1?\d{8,15}$", "Only integers are allowed"
        r"^(91|\+91)?-?[6789]\d{9}$",
        "Only valid format are allowed",
    )
    phone = serializers.CharField(
        required=True,
        max_length=16,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="mobile number already exist.",
            ),
            mobile_number_regex,
        ],
    )
    username = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=CustomUser.objects.all())]
    )
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            phone=validated_data["phone"]
        )

        return user

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "phone"
            ]


class SendOtpMobileSerailizer(serializers.Serializer):
    phone_regex = RegexValidator(r"^\+?1?\d{10,15}$", "Not a valid mobile number")
    phone = serializers.CharField(
        required=True, max_length=16, validators=[phone_regex]
    )

    def validate(self, attrs):
        if not CustomUser.objects.filter(phone=attrs.get("phone")):
            raise serializers.ValidationError(
                "We cannot find this mobile number in our database"
            )
        return super().validate(attrs)

    def create(self, validated_data):
        user, _ = CustomUser.objects.get_or_create(
            phone=validated_data["phone"]
        )
        return user




class VerifyOtpMobileSerailizer(serializers.Serializer):
    phone_regex = RegexValidator(r"^\+?1?\d{10,15}$", "Not a valid mobile number")
    phone = serializers.CharField(
        required=True, max_length=16, validators=[phone_regex]
    )
    otp = serializers.IntegerField()

    def validate(self, attrs):
        if not CustomUser.objects.get(phone=attrs.get("phone")):
            raise serializers.ValidationError(
                "We cannot find this mobile number in our database"
            )
        otp_verification = CustomUser.objects.filter(
            phone=attrs.get("phone")
        ).first()
        expire_time_start = datetime.now().replace(tzinfo=utc) - timedelta(seconds=300)
        if expire_time_start > otp_verification.created_at:
            raise serializers.ValidationError("OTP expired")
        if attrs.get("otp") != otp_verification.otp:
            raise serializers.ValidationError("Invalid Otp")
        otp_verification.otp = None
        otp_verification.save()
        return super().validate(attrs)

    def create(self, validated_data):
        user, _ = CustomUser.objects.get_or_create(
            phone=validated_data["phone"]
        )
        user.is_verified = True
        user.save()
        return user

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class AvailableCarsSerializer(serializers.ModelSerializer):
    vehicle_station = LocationSerializer()
    class Meta:
        model = CarDetails
        fields = "__all__"


class RentedCarsSerializer(serializers.ModelSerializer):
    car = AvailableCarsSerializer()
    class Meta:
        model = RentCar
        fields = "__all__"