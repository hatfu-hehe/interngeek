from django.urls import path
from . import views


urlpatterns = [
    path('task/', views.TaskViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
]

