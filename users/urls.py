from django.urls import path
from rest_framework import permissions

from users.apps import UsersConfig
from users.views import UserRetrieveUpdateDestroyView, UserCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('register/',
         UserCreateView.as_view(permission_classes=(permissions.AllowAny,)),
         name='register'),

    path('login/',
         TokenObtainPairView.as_view(
             permission_classes=(permissions.AllowAny,)
         ),
         name='login'),

    path('token/refresh/',
         TokenRefreshView.as_view(permission_classes=(permissions.AllowAny,)),
         name='token_refresh'),

    path('profile/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(),
         name='profile'),
    ]
