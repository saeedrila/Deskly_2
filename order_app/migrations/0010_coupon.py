# Generated by Django 4.2.1 on 2023-06-07 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0009_order_reward_points_order_shipping_cost_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=20)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('issued_quantity', models.PositiveIntegerField()),
                ('remaining_quantity', models.PositiveIntegerField()),
            ],
        ),
    ]