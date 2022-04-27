from django.db import models
import random
from django.conf import settings
from django.db.models import Q


class UserDetail(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    full_name = models.CharField(blank=True,max_length=40)
    
    class Meta:
        ordering=['-user_id']

class Email(models.Model):
    email = models.EmailField(primary_key=True)
    user_id =   models.ForeignKey(UserDetail,on_delete=models.CASCADE,related_name="emails") 

    
class Phone(models.Model):
    phone = models.CharField(max_length=12)
    user_id = models.ForeignKey(UserDetail,on_delete = models.CASCADE,related_name="phones")

    