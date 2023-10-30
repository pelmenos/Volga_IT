from django.urls import path

from .views import *

urlpatterns = [
    path('Transport/', RentTransportList.as_view()),
    path('<int:pk>', RetrieveRent.as_view()),
    path('MyHistory/', UserRentHistoryList.as_view()),
    path('TransportHistory/<int:pk>', TransportRentHistoryList.as_view()),
    path('New/<int:pk>', CreateRent.as_view()),
    path('End/<int:pk>', EndRent.as_view()),
]
