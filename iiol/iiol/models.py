from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
# Create your models here.


class Lib(models.Model):

    libcode = models.IntegerField(blank=False)
    libName = models.CharField(max_length=50)
    address = models.TextField()
    tel = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)
    latitue = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    homepage = models.models.TextField()
    closed = models.CharField(max_length=50)
    operatingTime = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

