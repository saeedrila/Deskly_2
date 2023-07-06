# Generated by Django 4.2.1 on 2023-07-05 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0010_category_is_active_subcategory_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='availability',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brand',
            name='offer_is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='brand',
            name='offer_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
    ]