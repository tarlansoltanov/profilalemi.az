# Generated by Django 4.2.1 on 2023-07-05 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('color', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Product Name',
                'verbose_name_plural': 'Product Names',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='color.color', verbose_name='Color')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.productname', verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]