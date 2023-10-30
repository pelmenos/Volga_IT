from django.urls import path

from .views import *

urlpatterns = [
    path('Me/', RetrieveUser.as_view(), name='get_user'),
    path('SignIn/', DecoratedTokenObtainPairView.as_view(), name='login_user'),
    path('SignUp/', RegisterUser.as_view(), name='register_user'),
    path('SignOut/', LogoutUser.as_view(), name='logout_user'),
    path('Update/', UpdateUser.as_view(), name='update_user'),
    path('Token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
]
