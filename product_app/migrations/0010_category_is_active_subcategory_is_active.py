# Generated by Django 4.2.1 on 2023-07-01 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0009_alter_product_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
