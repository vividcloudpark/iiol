# Generated by Django 4.0.5 on 2023-09-20 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_library_closed_alter_library_operatingtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='closed',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='library',
            name='operatingTime',
            field=models.TextField(),
        ),
    ]
