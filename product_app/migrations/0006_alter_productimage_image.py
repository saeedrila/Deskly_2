# Generated by Django 4.2.1 on 2023-06-10 10:30

from django.db import migrations, models
import product_app.models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0005_product_varient_subproduct_productimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.ImageField(
                upload_to=product_app.models.product_image_upload_to
            ),
        ),
    ]
