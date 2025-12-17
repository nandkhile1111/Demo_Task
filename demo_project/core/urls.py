from django.urls import path

from .views import (
    expense_list_create,
    expense_detail,
    weather_api,
    expense_report
)

urlpatterns = [
    path('expenses/', expense_list_create),
    path('expenses/<int:id>/', expense_detail),
    path('weather/<str:city>/', weather_api),  # city in the path
    path('report/', expense_report),
]
