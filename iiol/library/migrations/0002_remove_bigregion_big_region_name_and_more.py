# Generated by Django 4.0.5 on 2023-09-20 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bigregion',
            name='big_region_name',
        ),
        migrations.RemoveField(
            model_name='smallregion',
            name='small_region_name',
        ),
    ]
