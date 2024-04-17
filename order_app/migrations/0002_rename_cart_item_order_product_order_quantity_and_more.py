# Generated by Django 4.2.1 on 2023-05-24 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="cart_item",
            new_name="product",
        ),
        migrations.AddField(
            model_name="order",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
