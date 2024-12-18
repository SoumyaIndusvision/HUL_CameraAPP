from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "User"
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(null=True)
    username = models.CharField(max_length=100,blank=True,null=True, unique=True)
    created_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
