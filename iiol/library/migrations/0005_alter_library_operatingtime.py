# Generated by Django 4.0.5 on 2023-09-20 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_rename_libcode_library_libcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='operatingTime',
            field=models.CharField(max_length=100),
        ),
    ]
