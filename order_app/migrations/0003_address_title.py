# Generated by Django 4.2.1 on 2023-05-29 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0002_rename_cart_item_order_product_order_quantity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="title",
            field=models.CharField(default="", max_length=50),
        ),
    ]
