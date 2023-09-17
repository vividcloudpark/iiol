from django.db import models
from iiol.models import BaseTimeModel


def upload_to(instance, filename):
    return '/'.join(['media', str(instance.name), filename])


class Barcode(BaseTimeModel):
    lib_code = models.ForeignKey("library.Library",  on_delete=models.CASCADE)
    small_region_code = models.ForeignKey(
        "library.SmallRegion",  on_delete=models.CASCADE)
    # ISBN = models.models.ForeignKey("books.Book", on_delete=models.CASCADE)
