# Generated by Django 3.0 on 2020-01-13 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0034_auto_20200113_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bag',
            name='roll',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='factory.Roll'),
        ),
    ]