# Generated by Django 4.0.5 on 2023-10-13 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mybookwishlist', '0005_alter_mybookwishlist_deleted_mybookwishlistgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybookwishlist',
            name='groupname',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mybookwishlist.mybookwishlistgroup'),
        ),
    ]
