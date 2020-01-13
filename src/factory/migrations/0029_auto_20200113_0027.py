# Generated by Django 3.0 on 2020-01-12 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0028_auto_20200112_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='packingslips',
            name='block_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='packingslips',
            name='block_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='packingslips',
            name='block_unit',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='packingslips',
            name='print_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='packingslips',
            name='print_unit',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='packingslips',
            name='wcut_amount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='packingslips',
            name='wcut_weight',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='shipcart',
            name='bndl',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='shipcart',
            name='pricing',
            field=models.CharField(choices=[('basic', 'Basic'), ('colour', 'Colour'), ('w-cut', 'W-CUT')], default='basic', max_length=10),
        ),
    ]