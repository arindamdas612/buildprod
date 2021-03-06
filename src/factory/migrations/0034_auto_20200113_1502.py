# Generated by Django 3.0 on 2020-01-13 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import factory.models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20191214_0041'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distributor', '0001_initial'),
        ('factory', '0033_auto_20200113_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorytransactions',
            name='trxn_user',
            field=models.ForeignKey(default=factory.models.default_user, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='packingslips',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='distributor.Distributor'),
        ),
        migrations.AlterField(
            model_name='packingslips',
            name='prepared_by',
            field=models.ForeignKey(default=factory.models.default_user, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='roll',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='seller.Seller'),
        ),
        migrations.AlterField(
            model_name='shipcart',
            name='cart_owner',
            field=models.ForeignKey(default=factory.models.default_user, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
