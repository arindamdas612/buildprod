# Generated by Django 3.0 on 2020-01-05 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0016_auto_20191217_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roll',
            name='unit',
        ),
    ]
