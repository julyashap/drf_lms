from django.urls import path
from materials.apps import MaterialsConfig
from rest_framework import routers
from materials.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, CourseSubscribeManager, CourseSubscribeListAPIView

app_name = MaterialsConfig.name

router = routers.DefaultRouter()
router.register('', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/list/', LessonListAPIView.as_view(), name='list_lesson'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='retrieve_lesson'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='destroy_lesson'),

    path('course-subscribe/management/', CourseSubscribeManager.as_view(), name='manage_course_subscribe'),
    path('course-subscribe/list/', CourseSubscribeListAPIView.as_view(), name='list_course_subscribe'),
] + router.urls
