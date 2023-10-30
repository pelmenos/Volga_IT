from django.urls import path

from .views import *

urlpatterns = [
    path('', TransportListCreate.as_view()),
    path('<int:pk>', TransportDetail.as_view()),
]
