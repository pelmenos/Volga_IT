from django.urls import path

from .views import *

urlpatterns = [
    path('', AccountList.as_view()),
    path('<int:pk>', AccountDetail.as_view()),
]
