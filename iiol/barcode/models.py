from django.db import models


def upload_to(instance, filename):
    return '/'.join(['media', str(instance.name), filename])


class Barcode(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
