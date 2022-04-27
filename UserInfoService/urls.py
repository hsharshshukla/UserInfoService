from django.conf import settings
from django.urls import path, re_path,include
from django.contrib import admin

urlpatterns=[
    path('admin/', admin.site.urls),
    path('api/',include('user_details.urls')),
]