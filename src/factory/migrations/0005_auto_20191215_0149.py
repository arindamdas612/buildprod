# Generated by Django 3.0 on 2019-12-14 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0004_bag_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='bag',
            name='updated_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='roll',
            name='updated_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
