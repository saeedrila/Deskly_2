# Generated by Django 4.2.1 on 2023-05-24 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='brands')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='categories')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='sub_categories')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('mrp', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='products')),
                ('availability', models.BooleanField(default=False)),
                ('stock', models.CharField(max_length=50)),
                ('sell_count', models.CharField(default='0', max_length=10)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.subcategory')),
            ],
        ),
    ]
