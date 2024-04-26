# Generated by Django 4.1.7 on 2023-04-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spdapp', '0003_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'feedback_table',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Bike', 'Bike'), ('Car', 'Car'), ('Bike-Spareparts', 'Bike-Spareparts'), ('car-Spareparts', 'car-Spareparts'), ('Others', 'Others')], max_length=100),
        ),
    ]
