# Generated by Django 3.0 on 2020-01-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0022_auto_20200105_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='bag',
            name='status',
            field=models.CharField(choices=[('stocked', 'stocked'), ('in cart', 'In Cart'), ('shipped', 'Shipped')], default='stocked', max_length=10),
        ),
    ]
