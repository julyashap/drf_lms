from rest_framework import serializers
from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AnotherUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'city', 'phone']


class PaymentSerializer(serializers.ModelSerializer):
    user = AnotherUserSerializer()

    class Meta:
        model = Payment
        fields = ['date', 'sum', 'way', 'user', 'course', 'lesson']
