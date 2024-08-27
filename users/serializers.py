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
        fields = '__all__'


class PaymentCourseSerializer(serializers.ModelSerializer):
    user = AnotherUserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['date', 'sum', 'way', 'session_id', 'link', 'user', 'course']
        read_only_fields = ['date', 'sum', 'session_id', 'link']


class PaymentLessonSerializer(serializers.ModelSerializer):
    user = AnotherUserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['date', 'sum', 'way', 'session_id', 'link', 'user', 'lesson']
        read_only_fields = ['date', 'sum', 'session_id', 'link']


class PaymentStatusSerializer(serializers.Serializer):
    session_id = serializers.CharField()
