from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, PaymentCourseCreateAPIView, PaymentLessonCreateAPIView, \
    PaymentStatusAPIView

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='list_payment'),
    path('payments/course/create/', PaymentCourseCreateAPIView.as_view(), name='create_course_payment'),
    path('payments/lesson/create/', PaymentLessonCreateAPIView.as_view(), name='create_lesson_payment'),
    path('payments/status/', PaymentStatusAPIView.as_view(), name='status_payment'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
