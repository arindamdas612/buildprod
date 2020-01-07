from django.db import models
from django.utils.translation import gettext_lazy as _

from seller.models import Seller
from django.contrib.auth.models import User
from distributor.models import Distributor

# Create your models here.


class Roll(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    gsm = models.IntegerField()
    color = models.CharField(max_length=50)
    width = models.FloatField()
    weight = models.FloatField()
    length = models.FloatField(null=True)
    unit = models.IntegerField(null=True)
    stock_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.unit == 1:
            return f"{self.color} {self.gsm} GSM {self.width}'' {round(self.weight,2)} Kg {self.length} m {self.unit} unit"
        else:
            return f"{self.color} {self.gsm} GSM {self.width}'' {round(self.weight,2)} Kg {self.length} m {self.unit} units"


class Bag(models.Model):
    
    class BagType(models.TextChoices):
        D_TYPE = 'd-cut', _('d-cut')
        U_TYPE = 'u-cut', _('u-cut')
        HANDLE = 'handle', _('handle')
    
    class Status(models.TextChoices):
        STOCKED = 'stocked', _('stocked')
        CART = 'in cart', _('In Cart')
        SHIPPED = 'shipped', _('Shipped')

    roll = models.ForeignKey(Roll, on_delete=models.CASCADE)
    bag_type = models.CharField(max_length=10, choices=BagType.choices, default=BagType.D_TYPE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.STOCKED)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    width = models.FloatField(null=True)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.bag_type} {self.roll.color} {self.roll.gsm} GSM {self.height}'' X  {self.width}'' {self.weight} Kgs"


class Waste(models.Model):

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    weight = models.FloatField()
    create_timestamp = models.DateTimeField(auto_now_add=True)

class ShipCart(models.Model):
    class Pricing(models.TextChoices):
        BASIC = 'basic', _('Basic')
        COLUR = 'colour', _('Colour')

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(null=True)
    pricing = models.CharField(max_length=10, choices=Pricing.choices, default=Pricing.BASIC)
    cart_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bag}"

class PackingSlips(models.Model):
    party = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    
    basic_rate = models.FloatField(null=True)
    color_rate = models.FloatField(null=True)
    basic_weight = models.FloatField(null=True)
    color_weight = models.FloatField(null=True)
    
    basic_amount = models.FloatField(null=True)
    color_amount = models.FloatField(null=True)
    print_amount = models.FloatField(null=True)
    fare_amount = models.FloatField(null=True)
    advance_amount = models.FloatField(null=True)
    total_amount = models.FloatField(null=True)

    prepared_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_timestamp = models.DateTimeField(auto_now_add=True)


class Ship(models.Model):

    class Pricing(models.TextChoices):
        BASIC = 'basic', _('Basic')
        COLUR = 'colour', _('Colour')

    package = models.ForeignKey(PackingSlips, on_delete=models.CASCADE)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.00)
    pricing = models.CharField(max_length=10, choices=Pricing.choices, default=Pricing.BASIC)
    assingment_timestamp = models.DateTimeField(auto_now_add=True)

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
    



