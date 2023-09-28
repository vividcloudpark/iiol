# Generated by Django 4.0.5 on 2023-09-28 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode', '0001_squashed_0008_barcode_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='isbn13',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='barcode',
            name='statusCode',
            field=models.CharField(max_length=1),
        ),
    ]