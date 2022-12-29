from django.urls import path
from . import views


urlpatterns = [
    path(
        "user_register_view/",
        views.UserRegistrationView.as_view(),
        name="user_register_view",
    ),
    path(
        "send_otp/",
        views.SendMobileOtpView.as_view(),
        name="send_otp",
    ),
    path(
        "verify_otp/",
        views.VerifyMobileOtpView.as_view(),
        name="verify_otp",
    ),
    path(
        "available_cars_list/",
        views.AvailableCarsView.as_view(),
        name="available_cars_list",
    ),
    path(
        "single_car_view/<str:car_id>/",
        views.SingleCarView.as_view(),
        name="single_car_view",
    ),
    path(
        "rent_a_car/<str:car_id>/",
        views.RentACarView.as_view(),
        name="rent_a_car",
    ),
    path(
        "user_rented_cars/",
        views.UserRentedCarsView.as_view(),
        name="user_rented_cars",
    ),
    path(
        "rented_cars_location/<str:car_id>/",
        views.RentedCarLocationView.as_view(),
        name="rented_cars_location",
    ),
    path(
        "return_rented_car/",
        views.ReturnCarView.as_view(),
        name="return_rented_car",
    ),
]