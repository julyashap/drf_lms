from rest_framework import serializers
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'phone', 'city']


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Payment
        fields = ['date', 'sum', 'way', 'user', 'course', 'lesson']
