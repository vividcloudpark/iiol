# Generated by Django 4.0.5 on 2023-10-10 23:04

from django.db import migrations, models
import django.db.models.deletion


# def set_default_group_to_mybookwishlist(apps, schema_editor):
#     User = apps.get_model("accounts", "User")
#     Mybookwishlist = apps.get_model("mybookwishlist", "Mybookwishlist")
#     MybookwishlistGroup = apps.get_model("mybookwishlist", "MybookWishlistGroup")

#     MybookwishlistUpdate_obj = []
#     for user in User.objects.all():
#         temp_mybookwishlist_obj_qs = Mybookwishlist.objects.filter(user=user)
#         my_MybookwishlistGroup_pk = MybookwishlistGroup.objects.filter(user=user)[0]
#         for item in temp_mybookwishlist_obj_qs:
#             item.groupname = my_MybookwishlistGroup_pk
#             MybookwishlistUpdate_obj.append(item)

#     Mybookwishlist.objects.bulk_update(MybookwishlistUpdate_obj, ["groupname"])


class Migration(migrations.Migration):
    dependencies = [
        ("mybookwishlist", "0006_mybookwishlist_groupname"),
    ]

    operations = [
        migrations.AddField(
            model_name="mybookwishlist",
            name="groupname",
            field=models.ForeignKey(
                default=7,
                on_delete=django.db.models.deletion.PROTECT,
                to="mybookwishlist.mybookwishlistgroup",
            ),
            preserve_default=False,
        ),
        # migrations.RunPython(set_default_group_to_mybookwishlist),
    ]
