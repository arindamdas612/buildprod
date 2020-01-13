# Generated by Django 3.0 on 2020-01-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0018_roll_length'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bag',
            name='status',
        ),
        migrations.RemoveField(
            model_name='bag',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='roll',
            name='roll_type',
        ),
        migrations.AddField(
            model_name='bag',
            name='bag_type',
            field=models.CharField(choices=[('d-cut', 'd-cut'), ('u-cut', 'u-cut'), ('handle', 'handle')], default='d-cut', max_length=10),
        ),
        migrations.AddField(
            model_name='roll',
            name='unit',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bag',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]