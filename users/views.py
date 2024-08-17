from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from users.models import User, Payment
from users.permissions import IsCurrentUser
from users.serializers import UserSerializer, PaymentSerializer, AnotherUserSerializer


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
