from rest_framework import generics, viewsets
from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action != 'list':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        course = super().create(request, *args, **kwargs)
        course.owner = request.user
        course.save()
        return course

    def list(self, request, *args, **kwargs):
        courses = super().list(request, *args, **kwargs)
        if not self.request.user.groups.filter(name='moderators').exists():
            courses = courses.filter(owner=request.user)
        return courses


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

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
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
