from django.db import models
from iiol.models import BaseTimeModel


def upload_to(instance, filename):
    return '/'.join(['media', str(instance.name), filename])


class Barcode(BaseTimeModel):
    'libCode',
    'small_region_code',
    lib_code = models.ForeignKey("library.Library",  on_delete=models.CASCADE)
    small_region_code = models.ForeignKey(
        "library.SmallRegion",  on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=13)
