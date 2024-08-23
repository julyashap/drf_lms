from django.contrib import admin
from materials.models import Course, Lesson, CourseSubscribe


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'course',)


@admin.register(CourseSubscribe)
class CourseSubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'course', 'user',)
