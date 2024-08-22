from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(fields=['description', 'video'])]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, source='lesson_set.all', read_only=True)

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['name', 'description', 'count_lessons', 'lessons']
        validators = [LinkValidator(field='description')]
