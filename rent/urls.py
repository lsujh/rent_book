from django.urls import path

from .views import NewRent, RentListView

app_name = "rent"

urlpatterns = [
    path("new-rent/", NewRent.as_view(), name="new_rent"),
    path("", RentListView.as_view(), name="rent_list"),
]
