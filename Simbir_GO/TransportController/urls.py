from django.urls import path

from .views import *

urlpatterns = [
    path('<int:pk>', TransportDetail.as_view()),
    path('', CreateTransport.as_view()),
]
