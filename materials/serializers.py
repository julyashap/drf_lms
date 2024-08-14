from rest_framework import serializers
from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['name', 'description', 'count_lessons']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
