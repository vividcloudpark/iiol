# Generated by Django 4.0.5 on 2023-09-28 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybookwishlist', '0003_mybookwishlist_readyn_alter_mybookwishlist_memo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mybookwishlist',
            old_name='when_it_put',
            new_name='input_context',
        ),
        migrations.AddField(
            model_name='mybookwishlist',
            name='readDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
