from .models import Roll, Bag, Waste, InventoryTransactions


def waste_management(bag_id, roll_id, user):
    roll = Roll.objects.get(pk=roll_id)
    bag = Bag.objects.get(pk=bag_id)

    bag_trxn = InventoryTransactions(
        trxn_type=1,
        bag=bag,
        weight=bag.weight,
        unit=bag.unit,
        trxn_user=user
    )
    bag_trxn.save()

    bag_weight = bag.weight
    roll_weight = roll.weight

    bag_unit = bag.unit
    roll_unit = roll.unit

    waste_weight = round((((roll_weight/roll_unit) * bag_unit) - bag_weight),2)
    if waste_weight > 0:
        waste = Waste(bag=bag, weight=waste_weight)
        waste.save()

        waste_trxn = InventoryTransactions(
            trxn_type=2,
            waste=waste,
            weight = waste.weight,
            trxn_user=user
        )
        waste_trxn.save()
        
    roll.weight = roll_weight - bag_weight - waste_weight
    roll.unit = roll_unit - bag_unit
    roll.save()

    roll_use_trxn = InventoryTransactions(
        trxn_type=3,
        roll=roll,
        weight=round(((roll_weight/roll_unit)*bag_unit),2),
        unit=bag_unit,
        trxn_user=user
    )
    roll_use_trxn.save()
    
    

