from django.db import models
from iiol.models import BaseTimeModel
from django.contrib.auth import get_user_model

User = get_user_model()


def upload_to(instance, filename):
    return '/'.join(['media', str(instance.name), filename])


class Barcode(BaseTimeModel):
    small_region_code = models.ForeignKey(
        "library.SmallRegion",  on_delete=models.CASCADE)
    isbn13 = models.CharField(max_length=13)
    statusCode = models.CharField(max_length=1, blank=False)
    statusMsg = models.TextField(blank=True)
    user = models.BigIntegerField( blank=True, null=True)
    # UUID만들어서 각 여정별 트래킹?
