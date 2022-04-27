from django.contrib import admin
from .models import UserDetail,Email,Phone
# Register your models here.


admin.site.register(UserDetail)
admin.site.register(Phone)
admin.site.register(Email)
