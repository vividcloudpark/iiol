# Generated by Django 4.0.5 on 2023-09-20 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn13',
            field=models.CharField(db_index=True, max_length=13, primary_key=True, serialize=False, unique=True),
        ),
    ]
