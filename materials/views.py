from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, status
from rest_framework import views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from materials.models import Course, Lesson, CourseSubscribe
from materials.paginators import CourseLessonPaginator
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, CourseSubscribeSerializer, \
    CourseSubscribeRequestSerializer, CourseGetSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPaginator

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator]
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def list(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='moderators').exists():
            self.queryset = Course.objects.filter(owner=request.user)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CourseGetSerializer(page, many=True, context={'user': self.request.user})
            return self.get_paginated_response(serializer.data)
        serializer = CourseGetSerializer(queryset, many=True, context={'user': self.request.user})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CourseGetSerializer(instance, context={'user': self.request.user})
        return Response(serializer.data)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPaginator
    queryset = Lesson.objects.all()

    def get_queryset(self):
        if not self.request.user.groups.filter(name='moderators').exists():
            self.queryset = Lesson.objects.filter(owner=self.request.user)
        return super().get_queryset()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class CourseSubscribeManager(views.APIView):

    @swagger_auto_schema(
        responses={
            201: CourseSubscribeSerializer(),
            204: openapi.Response("Подписка удалена!")
        },
        request_body=CourseSubscribeRequestSerializer()
    )
    def post(self, *args, **kwargs):
        user = self.request.user

        serializer = CourseSubscribeRequestSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        course_pk = serializer.validated_data['course']
        course = get_object_or_404(Course, pk=course_pk)

        course_subscribe = CourseSubscribe.objects.filter(user=user, course=course)

        if not course_subscribe:
            new_course_subscribe = CourseSubscribe.objects.create(user=user, course=course)
            new_course_subscribe.save()

            course_subscribe_serializer = CourseSubscribeSerializer(new_course_subscribe)
            response = Response(course_subscribe_serializer.data, status=status.HTTP_201_CREATED)
        else:
            course_subscribe.delete()
            response = Response({"message": "Подписка удалена!"}, status=status.HTTP_204_NO_CONTENT)

        return response


class CourseSubscribeListAPIView(generics.ListAPIView):
    serializer_class = CourseSubscribeSerializer
    queryset = CourseSubscribe.objects.all()
