from rest_framework import serializers
from materials.models import Course, Lesson, CourseSubscribe
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(fields=['description', 'video'])]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, source='lesson_set.all', read_only=True)
    is_user_subscribe = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    def get_is_user_subscribe(self, obj):
        user = self.context['user']
        course_subscribe = CourseSubscribe.objects.filter(user=user, course=obj)

        if not course_subscribe:
            is_user_subscribe = "Подписка неактивна"
        else:
            is_user_subscribe = "Подписка активна"

        return is_user_subscribe

    class Meta:
        model = Course
        fields = ['pk', 'name', 'description', 'count_lessons', 'lessons', 'is_user_subscribe']
        validators = [LinkValidator(field='description')]


class CourseSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscribe
        fields = '__all__'
