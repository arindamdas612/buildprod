from django.db import models
from django.utils.translation import gettext_lazy as _

from seller.models import Seller
from django.contrib.auth.models import User
from distributor.models import Distributor

# Create your models here.


class Roll(models.Model):

    class RollType(models.TextChoices):
        D_TYPE = 'd', _('d-type rolls')
        U_TYPE = 'u', _('u-type rolls')

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    gsm = models.IntegerField()
    color = models.CharField(max_length=50)
    roll_type = models.CharField(max_length=2, choices=RollType.choices, default=RollType.D_TYPE)
    width = models.FloatField()
    weight = models.FloatField()
    unit = models.IntegerField()
    stock_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.color} {self.gsm} GSM {self.width}'' {round(self.weight,2)} Kg {self.unit} Unit(s) [{self.roll_type}-type]"


class Bag(models.Model):
    
    class State(models.TextChoices):
        STOCKED = 'STOCKED', _('In Stock')
        SHIPPED = 'SHIPPED', _('Shipped')

    roll = models.ForeignKey(Roll, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=State.choices, default=State.STOCKED)
    weight = models.FloatField()
    unit = models.IntegerField()
    create_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.roll.color} {self.roll.gsm} GSM {self.roll.width}'' [{self.unit} unit(s)]"


class Waste(models.Model):

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    weight = models.FloatField()
    create_timestamp = models.DateTimeField(auto_now_add=True)


class Ship(models.Model):

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    assingment_timestamp = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)


class InventoryTransactions(models.Model):
    trxn_type = models.IntegerField()
    roll = models.ForeignKey(Roll, on_delete=models.CASCADE, null=True)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, null=True)
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE, null=True)
    waste = models.ForeignKey(Waste, on_delete=models.CASCADE, null=True)
    weight = models.FloatField()
    unit = models.IntegerField(null=True)
    trxn_user = models.ForeignKey(User, on_delete=models.CASCADE)
    trxn_timestamp = models.DateTimeField(auto_now_add=True)