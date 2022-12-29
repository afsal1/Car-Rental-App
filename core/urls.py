from django.urls import path
from . import views


urlpatterns = [
    path(
        "admin_login/",
        views.AdminLoginView.as_view(),
        name="admin_login",
    ),
    path(
        "add_or_get_locations/",
        views.LocationAddView.as_view(),
        name="add_or_get_locations",
    ),
    path(
        "delete_location/<str:location_id>/",
        views.LocationAddView.as_view(),
        name="delete_location",
    ),
    path(
        "add_or_get_cars/",
        views.CarAddView.as_view(),
        name="add_or_get_cars",
    ),
    path(
        "delete_car/<str:car_id>/",
        views.CarAddView.as_view(),
        name="delete_car",
    ),
    path(
        "update_car/<str:car_id>/",
        views.UpdateCarView.as_view(),
        name="update_car",
    ),
]