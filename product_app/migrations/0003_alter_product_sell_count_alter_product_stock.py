# Generated by Django 4.2.1 on 2023-06-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0002_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sell_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
