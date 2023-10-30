from django.urls import path

from .views import *

urlpatterns = [
    path('Rent/<int:pk>', RentDetail.as_view()),
    path('UserHistory/<int:pk>', UserRentHistory.as_view()),
    path('TransportHistory/<int:pk>', TransportRentHistory.as_view()),
    path('Rent/', CreateRent.as_view()),
    path('Rent/End/<int:pk>', EndRent.as_view()),
]
