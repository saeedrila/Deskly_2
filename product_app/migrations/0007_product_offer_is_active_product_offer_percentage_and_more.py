# Generated by Django 4.2.1 on 2023-06-12 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0006_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='offer_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subproduct',
            name='offer_is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subproduct',
            name='offer_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
    ]