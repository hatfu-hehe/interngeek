from . import swagger
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/tasks/', include ('app.urls'))
]

urlpatterns += swagger.urlpatterns
