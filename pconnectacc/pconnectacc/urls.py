from django.contrib import admin
from django.urls import path, include
from taskcontrol import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task-control/', include('taskcontrol.urls')),
]

handler404 = 'taskcontrol.views.handler404'