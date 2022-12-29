from rest_framework.views import APIView
from utilities.mixins import HttpResponseMixin
from .serializers import LocationSerializer, AvailableCarsSerializer,\
    AdminLoginSerializer
from . models import Location, CarDetails


class AdminLoginView(APIView, HttpResponseMixin):
    """
    Class Name: AdminLoginView
    description: Manage admin login
    """

    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        """
        Function Name : post
        Description: admin login
        params: email, password
        return: access_token,refresh_token,user_details
        """
        serializer = AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            return self.success_response(
                code="HTTP_200_OK", data=serializer.validated_data, 
                message="admin logined Successfully"
            )
        return self.error_response(
            code="HTTP_400_BAD_REQUEST", 
            message="Something went wrong",
            error=serializer.errors,
        )

    
class LocationAddView(APIView, HttpResponseMixin):
    """
    Class Name: LocationAddView
    description: Manage location of the admin
    """
    serializer_class = LocationSerializer
    def post(self, request):
        """
        Function Name : post
        Description: to add location
        params: vehicle_station
        return: success response
        """

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return self.success_response(
                    message="location added",
                    code="HTTP_201_CREATED",
                    data=serializer.data,
                )
            return self.error_response(
                message="something missing", code="HTTP_400_BAD_REQUEST"
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )

    def get(self, request):
        """
        Function Name : get
        Description: to get all the location of the admin
        params: no
        return: all the locations
        """
        try:
            user = request.user
            location = Location.objects.filter(user=user)
            serializer = self.serializer_class(location, many=True)
            return self.success_response(
                message="admin vehicle locations", 
                code="HTTP_200_OK", data=serializer.data
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


    def delete(self, request, *args, **kwargs):
        """
        Function Name : delete
        Description: to delete selected location of the admin
        params: location_id
        return: success response
        """
        try:
            try:
                location = Location.objects.get(id=kwargs.get("location_id"))
            except Exception as e:
                return self.error_response(
                    code="HTTP_400_BAD_REQUEST", message=f"Invalid location id"
                )
            location.delete()
            return self.success_response(
                code="HTTP_200_OK", message="location deleted successfully"
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class CarAddView(APIView, HttpResponseMixin):
    """
    Class Name: CarAddView
    description: Manage cars of the admin
    """
    serializer_class = AvailableCarsSerializer
    
    def post(self, request):
        """
        Function Name : post
        Description: to add cars
        params: car_name, day_price, car_image
                vehicle_station
        return: success response
        """

        try:
            admin = request.user
            car_name = request.data["car_name"]
            day_price = request.data["day_price"]
            car_image = request.data["car_image"]
            vehicle_station = Location.objects.get(id=request.data["location"])


            CarDetails.objects.create(
                user=admin,
                car_name=car_name,
                day_price=day_price,
                car_image=car_image,
                vehicle_station=vehicle_station
            )

            return self.success_response(
                message="car added",
                code="HTTP_201_CREATED"
            )
        
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )

    def get(self, request):
        """
        Function Name : get
        Description: to get all the cars of the admin
        params: no
        return: all the cars
        """
        try:
            user = request.user
            car_details = CarDetails.objects.filter(user=user)
            serializer = self.serializer_class(car_details, many=True)
            return self.success_response(
                message="admin vehicle details", 
                code="HTTP_200_OK", data=serializer.data
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


    def delete(self, request, *args, **kwargs):
        """
        Function Name : delete
        Description: to delete selected car of the admin
        params: car_id
        return: success response
        """
        try:
            try:
                car = CarDetails.objects.get(id=kwargs.get("car_id"))
            except Exception as e:
                return self.error_response(
                    code="HTTP_400_BAD_REQUEST", message=f"Invalid car id"
                )
            car.delete()
            return self.success_response(
                code="HTTP_200_OK", message="car deleted successfully"
            )
        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )


class UpdateCarView(APIView, HttpResponseMixin):
    """
    Class Name: UpdateCarView
    description: update cars of the admin
    """
    def put(self, request, *args, **kwargs):
        """
        Function Name : put
        Description: admin can update car details
        params: car_id
        return: success response
        """
        try:
            car = CarDetails.objects.get(id=kwargs.get("car_id"))
            data = request.data

            location = (
                data["vehicle_station"] if data.get("vehicle_station", None) else car.vehicle_station
            )

            car.car_name = (
                data["car_name"] if data.get("car_name", None) else car.car_name
            )

            car.day_price = (
                data["day_price"]
                if data.get("day_price", None)
                else car.day_price
            )

            car.car_image = (
                data["car_image"]
                if data.get("car_image", None)
                else car.car_image
            )

            if data.get("vehicle_station", None):
                car.vehicle_station = Location.objects.get(id=location)

            car.save()

            return self.success_response(
                code="HTTP_200_OK", message="car details updated successfully"
            )

        except Exception as e:
            return self.error_response(
                code="HTTP_400_BAD_REQUEST",
                message=f"Something went wrong, Exact Problem: {e}",
            )
