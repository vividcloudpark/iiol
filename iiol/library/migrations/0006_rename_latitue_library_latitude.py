# Generated by Django 4.0.5 on 2023-09-20 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_library_operatingtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='library',
            old_name='latitue',
            new_name='latitude',
        ),
    ]
