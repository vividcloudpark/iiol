from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
# Create your models here.


class BaseTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    DELETED = models.BooleanField(default=False)

    class Meta:
        abstract = True
