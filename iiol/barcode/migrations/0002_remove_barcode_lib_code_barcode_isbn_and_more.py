# Generated by Django 4.2.5 on 2023-09-27 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcode',
            name='lib_code',
        ),
        migrations.AddField(
            model_name='barcode',
            name='ISBN',
            field=models.CharField(default=1, max_length=13),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='barcode',
            name='statusCode',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='barcode',
            name='statusMsg',
            field=models.TextField(blank=True),
        ),
    ]
