# Generated by Django 4.0.2 on 2023-08-26 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cabs', '0003_cars_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=6)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='cars',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.IntegerField(blank=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_user', to=settings.AUTH_USER_MODEL)),
                ('end_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_end_point', to='cabs.city')),
                ('start_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_start_point', to='cabs.city')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
