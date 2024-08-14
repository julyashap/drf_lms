from django.urls import path
from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='list_user'),
    path('update/<int:pk>', UserUpdateAPIView.as_view(), name='update_user'),
]
