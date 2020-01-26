from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from seller.models import Seller
from django.contrib.auth.models import User
from distributor.models import Distributor

# Create your models here.

def default_user():
    return User.objects.get(pk=1)


class Roll(models.Model):
    class PrintType(models.TextChoices):
        NORMAL = 'Normal', _('Normal')
        FLEXO = 'Flexo', _('Flexo')

    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    gsm = models.IntegerField()
    color = models.CharField(max_length=50)
    print_type = models.CharField(max_length=10, choices=PrintType.choices, default=PrintType.NORMAL)
    width = models.FloatField()
    weight = models.FloatField()
    length = models.FloatField(null=True)
    unit = models.IntegerField(null=True)
    stock_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.unit == 1:
            return f"{self.print_type} {self.color} {self.gsm} GSM {self.width}'' {round(self.weight,2)} Kg {self.length} m {self.unit} unit"
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

    class PrintType(models.TextChoices):
        NORMAL = 'Normal', _('Normal')
        OFFSET = 'Offset', _('Offset')

    roll = models.ForeignKey(Roll, on_delete=models.CASCADE, null=True)
    bag_type = models.CharField(max_length=10, choices=BagType.choices, default=BagType.D_TYPE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.STOCKED)
    print_type = models.CharField(max_length=10, choices=PrintType.choices, default=PrintType.NORMAL)
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
        COLOR = 'colour', _('Colour')
        WCUT = 'w-cut', _('W-CUT')

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(null=True)
    bndl = models.FloatField(null=True)
    pricing = models.CharField(max_length=10, choices=Pricing.choices, default=Pricing.BASIC)
    remarks = models.CharField(max_length=30, default='')
    cart_owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bag}"

class PackingSlips(models.Model):
    party = models.ForeignKey(Distributor, on_delete=models.SET_NULL, null=True, blank=True)
    
    basic_rate = models.FloatField(null=True)
    color_rate = models.FloatField(null=True)
    wcut_rate = models.FloatField(null=True)

    basic_weight = models.FloatField(null=True)
    color_weight = models.FloatField(null=True)
    wcut_weight = models.FloatField(null=True)
    
    basic_amount = models.FloatField(null=True)
    color_amount = models.FloatField(null=True)
    wcut_amount = models.FloatField(null=True)

    print_unit = models.FloatField(null=True)
    print_rate = models.FloatField(null=True)
    print_amount = models.FloatField(null=True)

    block_unit = models.FloatField(null=True)
    block_rate = models.FloatField(null=True)
    block_amount = models.FloatField(null=True)
    
    fare_amount = models.FloatField(null=True)
    
    advance_amount = models.FloatField(null=True)
    
    total_amount = models.FloatField(null=True)

    prepared_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)
    create_timestamp = models.DateTimeField(auto_now_add=True)


class Ship(models.Model):

    class Pricing(models.TextChoices):
        BASIC = 'basic', _('Basic')
        COLOR = 'colour', _('Colour')
        WCUT = 'w-cut', _('W-CUT')

    package = models.ForeignKey(PackingSlips, on_delete=models.CASCADE)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.00)
    bndl = models.FloatField(default=0.00)
    remarks = models.CharField(max_length=30, default='')
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
    trxn_user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=default_user)
    trxn_timestamp = models.DateTimeField(auto_now_add=True)
    



