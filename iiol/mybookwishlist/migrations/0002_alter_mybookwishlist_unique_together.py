# Generated by Django 4.2.5 on 2023-09-27 12:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0004_alter_book_bookimageurl_alter_book_class_nm_and_more'),
        ('mybookwishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mybookwishlist',
            unique_together={('user', 'isbn13')},
        ),
    ]
