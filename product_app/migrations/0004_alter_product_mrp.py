# Generated by Django 4.2.1 on 2023-06-08 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_alter_product_sell_count_alter_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='mrp',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
