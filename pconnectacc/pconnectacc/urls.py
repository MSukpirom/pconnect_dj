from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('task-control/', include('taskcontrol.urls')),
    path('accounts-user/', include('user.urls')),
]
