# Generated by Django 4.0.5 on 2023-09-20 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_isbn13'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.CharField(default=2020, max_length=20),
            preserve_default=False,
        ),
    ]
