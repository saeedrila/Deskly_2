# Generated by Django 4.2.1 on 2023-06-07 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order_app", "0010_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
