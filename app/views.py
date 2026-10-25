from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskDetailsSerializer, TaskListSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskDetailsSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.kwargs.get('id') is None:
            return TaskListSerializer
        return TaskDetailsSerializer

    def list(self, request, *args, **kwargs):
        cached_data = cache.get("tasks_list")
        if cached_data:
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().list(request, *args, **kwargs)
        if response.data.get("total", 0) > 0:
            cache.set("tasks_list", response.data, timeout=30)
        return response

    def create(self, request, *args, **kwargs):
        serializer = TaskDetailsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        task = Task.objects.create(
            title=serializer.validated_data.get('title'),
            description=serializer.validated_data.get('description'),
            status=serializer.validated_data.get('status'),
            category=serializer.validated_data.get('category'),
        )
        return Response(status=status.HTTP_201_CREATED,
                        data=TaskDetailsSerializer(task).data)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskDetailsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        task.title = serializer.validated_data.get('title')
        task.description = serializer.validated_data.get('description')
        task.category = serializer.validated_data.get('category')
        task.status = serializer.validated_data.get('status')
        task.save()
        return Response(status=status.HTTP_200_OK,
                        data=TaskDetailsSerializer(task).data)