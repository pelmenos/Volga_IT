from django.urls import path

from .views import *

urlpatterns = [
    path('<int:pk>', IncreaseBalance.as_view()),
]
