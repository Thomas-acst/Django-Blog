from django.db import models
from django.contrib.auth.models import AbstractUser


class Info_User(AbstractUser):
    nickname = models.CharField(max_length=20)
    nascimento = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=30)
