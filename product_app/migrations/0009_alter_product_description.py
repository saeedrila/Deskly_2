# Generated by Django 4.2.1 on 2023-06-19 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0008_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(),
        ),
    ]
