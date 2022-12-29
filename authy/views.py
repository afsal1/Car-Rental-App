from rest_framework.views import APIView
from utilities.mixins import HttpResponseMixin
import random
from . import serializers
from datetime import datetime
from .common import send_otp
from utilities.jwt_handler import get_tokens_for_user
from core.models import CarDetails, RentCar, Location
from datetime import date

import pytz
utc = pytz.UTC


class UserRegistrationView(APIView, HttpResponseMixin):
    """
    Class Name: UserRegistrationView
    description: Manage user registration
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Function Name : post
        Description: user registration
        params: phone, password
        return: access_token,refresh_token,user_details
        """
        try:
            
            otp = random.randint(100000, 999999)
            serializer = serializers.UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.otp = otp
                user.created_at = datetime.now().replace(tzinfo=utc)
                user.save()
                send_otp(
                    otp,
                    user.phone
                )
                return self.success_response(
                        message="User registered and Otp Sent successfully", code="HTTP_200_OK"
                    )
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message="Something went wrong",
                error=serializer.errors,
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class SendMobileOtpView(APIView, HttpResponseMixin):
    """
    Class Name: SendMobileOtpView
    description: send mobile otp
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Function Name : post
        Description: send otp to mobile number
        params: phone
        return: success response
        """
        try:
            phone = request.data.get("phone")
            otp = random.randint(100000, 999999)
            serializer = serializers.SendOtpMobileSerailizer(data=request.data)
            if serializer.is_valid():
                otp_verification = serializer.save()
                otp_verification.otp = otp
                otp_verification.created_at = datetime.now().replace(tzinfo=utc)
                otp_verification.save()

                send_otp(
                    otp,
                    phone
                )
                return self.success_response(
                        message="Otp Sent successfully", code="HTTP_200_OK"
                    )
            return self.error_response(
                    code="HTTP_400_BAD_REQUEST",
                    message="Error sending otp to this mobile number",
                    error=serializer.errors,
                )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class VerifyMobileOtpView(APIView, HttpResponseMixin):
    """
    Class Name: VerifyMobileOtpView
    description: verify otp sended to user mobile number
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Function Name : post
        Description: send otp to mobile number
        params: phone, otp --> phone number not need to given
                by user , taken it from FE
        return: success response
        """
        serializer = serializers.VerifyOtpMobileSerailizer(data=request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                if user.is_verified:
                    tokens = get_tokens_for_user(user)
                    data = {
                        "id": user.id,
                        "access_token": tokens.get("access_token"),
                        "refresh_token": tokens.get("refresh_token"),
                    }

                    return self.success_response(
                        code="HTTP_200_OK",
                        message="OTP matched successfully", data=data
                    )

                return self.error_response(
                    code="HTTP_400_BAD_REQUEST", message="User is not verified"
                )

            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message="Otp verifying failed",
                error=serializer.errors,
            )

        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class AvailableCarsView(APIView, HttpResponseMixin):
    """
    Class Name: AvailableCarsView
    description: available cars to rent
    """
    def get(self, request):
        """
        Function Name : get
        Description: list available cars to rent user
        params: no
        return: available cars list
        """
        try:
            car = CarDetails.objects.filter(is_available=True)
            serializer = serializers.AvailableCarsSerializer(car, many=True)
            return self.success_response(
                code="HTTP_200_OK",
                message="available cars listed", data=serializer.data
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class QRCodeView(APIView, HttpResponseMixin):
    """
    Class Name: QRCodeView
    description: to view the qr code of the car
    """
    def get(self, request, *args, **kwargs):
        """
        Function Name : get
        Description: to view the qr code of the car
        params: car_id
        return: car details
        """
        try:
            car = CarDetails.objects.get(id=kwargs.get("car_id"))
            serializer = serializers.QRCodeSerializer(car)
            return self.success_response(
                code="HTTP_200_OK",
                message="car detail view", data=serializer.data
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class SingleCarView(APIView, HttpResponseMixin):
    """
    Class Name: SingleCarView
    description: to detail view of single car
    """
    def get(self, request, *args, **kwargs):
        """
        Function Name : get
        Description: detail view of single car
        params: car_id
        return: car details
        """
        try:
            car = CarDetails.objects.get(id=kwargs.get("car_id"))
            serializer = serializers.AvailableCarsSerializer(car)
            return self.success_response(
                code="HTTP_200_OK",
                message="car detail view", data=serializer.data
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class RentACarView(APIView, HttpResponseMixin):
    """
    Class Name: RentACarView
    description: to rent a car
    """
    def post(self, request, *args, **kwargs):
        """
        Function Name : post
        Description: rent a car from this view
        params: car_id
        return: success response
        """
        try:
            car = CarDetails.objects.get(id=kwargs.get("car_id"))
            
            rented_car = RentCar(
            user=request.user,
            car=car,
            rented_date=date.today()
            )
            rented_car.save()
            car.is_available = False
            car.save()
            return self.success_response(
                code="HTTP_200_OK",
                message="car rented successfully"
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class UserRentedCarsView(APIView, HttpResponseMixin):
    """
    Class Name: UserRentedCarsView
    description: to view user rented cars
    """
    def get(self, request):
        """
        Function Name : get
        Description: list of user rented cars
        params: no
        return: user rented car details
        """
        try:
            rented_cars = RentCar.objects.filter(user=request.user)
            serializer = serializers.RentedCarsSerializer(rented_cars, many=True)
            return self.success_response(
                code="HTTP_200_OK",
                message="user rented cars successfully",
                data=serializer.data
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class RentedCarLocationView(APIView, HttpResponseMixin):
    """
    Class Name: RentedCarLocationView
    description: list of rented car location
    """
    def get(self, request, *args, **kwargs):
        """
        Function Name : get
        Description: user rented cars related locations
        params: car_id
        return: location details
        """
        try:
            try:    
                rented_car = RentCar.objects.get(id=kwargs.get("car_id"))
            except Exception as e:
                return self.error_response(
                    code="HTTP_400_BAD_REQUEST",
                    message="invalid rent car id",
                )
            location = rented_car.car.vehicle_station
            serializer = serializers.LocationSerializer(location)
            return self.success_response(
                    code="HTTP_200_OK",
                    message="rented cars locations",
                    data=serializer.data
                )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class ReturnCarView(APIView, HttpResponseMixin):
    """
    Class Name: ReturnCarView
    description: to return a car that rented by user
    """
    def post(self, request):
        """
        Function Name : post
        Description: return a car that rented by user
        params: car_id, location_id
        return: success response
        """
        try:
            rented_car = RentCar.objects.get(id=request.data["car_id"])
            location = Location.objects.get(id=request.data["location_id"])
            rented_car.return_date = date.today()
            rented_car.car.is_available = True
            rented_car.car.vehicle_station = location
            rented_car.save()
            total_days = (rented_car.return_date - rented_car.rented_date).days
            rent = total_days*( rented_car.car.day_price)
            data = {
                "rented car price": rent
            }
            return self.success_response(
                    code="HTTP_200_OK",
                    message="rented cars returned",
                    data=data
                )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )