from .models import Roll, Bag, Waste, InventoryTransactions, PackingSlips, ShipCart, Bag, Ship

def waste_management(bag_id, roll_id, user, roll_weight, waste_weight):
    roll_weight = float(roll_weight)
    waste_weight = float(waste_weight)
    roll = Roll.objects.get(pk=roll_id)
    bag = Bag.objects.get(pk=bag_id)

    bag.weight = round((roll_weight - waste_weight),3)
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

    roll.weight = round((roll.weight - roll_weight),3)
    roll.unit = roll.unit - 1

    roll.save()

    roll_use_trxn = InventoryTransactions(
        trxn_type=3,
        roll=roll,
        weight=roll_weight,
        trxn_user=user
    )
    roll_use_trxn.save()

def ship_package(ps_id, user):
    package = PackingSlips.objects.get(pk=ps_id)
    user_cart = ShipCart.objects.filter(cart_owner=user)

    basic_weight = 0
    color_weight = 0

    for cart_item in user_cart:
        if cart_item.pricing == 'basic':
            basic_weight+=cart_item.weight
        if cart_item.pricing == 'colour':
            color_weight+=cart_item.weight
        
        bag = cart_item.bag
        bag.weight-=cart_item.weight
        bag.status= 'shipped' if bag.weight == 0 else 'stocked'
        bag.save()

        shipment = Ship(package=package,
                        bag=bag,
                        weight=cart_item.weight,
                        pricing=cart_item.pricing)
        shipment.save()
        cart_item.delete()
    
    package.basic_amount = round((package.basic_rate * basic_weight),2)
    package.color_amount = round((package.color_rate * color_weight),2)

    package.total_amount = package.basic_amount + package.color_amount + \
                            package.print_amount + package.fare_amount - \
                                package.advance_amount
    package.save()
    return True

        

        


    

