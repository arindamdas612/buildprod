from django.contrib import admin
from .models import Roll, Bag, Waste, Ship, ShipCart, PackingSlips
# Register your models here.


admin.site.register(Roll)
admin.site.register(Bag)
admin.site.register(Waste)
admin.site.register(Ship)
admin.site.register(ShipCart)
admin.site.register(PackingSlips)