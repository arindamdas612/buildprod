from .models import Roll, Bag, Waste, InventoryTransactions


def waste_management(bag_id, roll_id, user, roll_weight, waste_weight):
    roll_weight = int(roll_weight)
    waste_weight = int(waste_weight)
    roll = Roll.objects.get(pk=roll_id)
    bag = Bag.objects.get(pk=bag_id)

    bag.weight = roll_weight - waste_weight
    bag.save()

    bag_trxn = InventoryTransactions(
        trxn_type=1,
        bag=bag,
        weight=bag.weight,
        trxn_user=user
    )
    bag_trxn.save()

    waste = Waste(bag=bag, weight=waste_weight)
    waste.save()

    waste_trxn = InventoryTransactions(
        trxn_type=2,
        waste=waste,
        weight = waste.weight,
        trxn_user=user
    )
    waste_trxn.save()

    roll.weight = roll.weight - roll_weight
    roll.unit = roll.unit - 1

    roll.save()

    roll_use_trxn = InventoryTransactions(
        trxn_type=3,
        roll=roll,
        weight=roll_weight,
        trxn_user=user
    )
    roll_use_trxn.save()
    
    

