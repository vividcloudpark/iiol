# Generated by Django 4.2.5 on 2023-09-27 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybookwishlist', '0002_alter_mybookwishlist_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybookwishlist',
            name='readYn',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mybookwishlist',
            name='memo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mybookwishlist',
            name='when_it_put',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]