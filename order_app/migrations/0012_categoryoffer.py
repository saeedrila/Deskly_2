# Generated by Django 4.2.1 on 2023-06-08 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0011_coupon_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
