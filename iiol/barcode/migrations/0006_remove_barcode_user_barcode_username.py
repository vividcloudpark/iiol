# Generated by Django 4.2.5 on 2023-09-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode', '0005_alter_barcode_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barcode',
            name='user',
        ),
        migrations.AddField(
            model_name='barcode',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]