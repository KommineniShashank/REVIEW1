# Generated by Django 4.1.7 on 2023-05-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spdapp', '0007_delete_cartproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Bike-Spareparts', 'Bike-Spareparts'), ('car-Spareparts', 'car-Spareparts'), ('Others', 'Others')], max_length=100),
        ),
    ]