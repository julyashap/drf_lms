import datetime
import stripe
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pytz import timezone
from rest_framework import generics, viewsets, views, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from config import settings
from users.models import User, Payment
from users.permissions import IsCurrentUser
from users.serializers import UserSerializer, PaymentSerializer, AnotherUserSerializer, PaymentCourseSerializer, \
    PaymentLessonSerializer, PaymentStatusSerializer, CustomTokenObtainPairSerializer
from users.services import perform_create_payment
from rest_framework_simplejwt.views import (TokenObtainPairView as BaseTokenObtainPairView,
                                            TokenRefreshView as BaseTokenRefreshView)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsCurrentUser]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        if request.user != self.get_object():
            self.serializer_class = AnotherUserSerializer
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.serializer_class = AnotherUserSerializer
        return super().list(request, *args, **kwargs)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ('course', 'lesson', 'way',)


class PaymentCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCourseSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        course_payment = serializer.save(user=self.request.user, date=datetime.datetime.now(
            tz=timezone(settings.TIME_ZONE)))
        perform_create_payment(course_payment, course_payment.course.price, course_payment.course.name)


class PaymentLessonCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentLessonSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        lesson_payment = serializer.save(user=self.request.user, date=datetime.datetime.now(
            tz=timezone(settings.TIME_ZONE)))
        perform_create_payment(lesson_payment, lesson_payment.lesson.price, lesson_payment.lesson.name)


class PaymentStatusAPIView(views.APIView):

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Payment status")
        },
        request_body=PaymentStatusSerializer()
    )
    def post(self, *args, **kwargs):
        serializer = PaymentStatusSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data['session_id']

        payment_status = stripe.checkout.Session.retrieve(session_id)

        return Response({'status': payment_status.get('status')}, status=status.HTTP_200_OK)


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TokenRefreshView(BaseTokenRefreshView):
    pass
