# Generated by Django 4.2.1 on 2023-05-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0004_remove_address_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="title",
            field=models.CharField(default="Title", max_length=50),
        ),
    ]
