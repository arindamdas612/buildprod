# Generated by Django 3.0 on 2020-01-07 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distributor', '0001_initial'),
        ('factory', '0023_bag_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackingSlips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_rate', models.FloatField(null=True)),
                ('color_rate', models.FloatField(null=True)),
                ('basic_weight', models.FloatField(null=True)),
                ('color_weight', models.FloatField(null=True)),
                ('basic_amount', models.FloatField(null=True)),
                ('color_amount', models.FloatField(null=True)),
                ('print_amount', models.FloatField(null=True)),
                ('fare_amount', models.FloatField(null=True)),
                ('advance_amount', models.FloatField(null=True)),
                ('total_amount', models.FloatField(null=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributor.Distributor')),
                ('prepared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
