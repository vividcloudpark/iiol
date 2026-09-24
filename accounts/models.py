from django.contrib.auth.models import AbstractUser
from django.db import models

from .regions import region_choices


class User(AbstractUser):
    email = models.EmailField(unique=True)
    region_code = models.CharField(max_length=5, choices=region_choices())

    def __str__(self):
        return self.username
