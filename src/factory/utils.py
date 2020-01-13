from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa
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
    wcut_weight = 0

    for cart_item in user_cart:
        if cart_item.pricing == 'basic':
            basic_weight+=cart_item.weight
        if cart_item.pricing == 'colour':
            color_weight+=cart_item.weight
        if cart_item.pricing == 'wcut':
            wcut_weight+=cart_item.weight
        
        bag = cart_item.bag
        bag.weight= round((bag.weight - cart_item.weight),2)
        bag.status= 'shipped' if bag.weight == 0 else 'stocked'
        bag.save()

        shipment = Ship(package=package,
                        bag=bag,
                        weight=cart_item.weight,
                        bndl=cart_item.bndl,
                        remarks=cart_item.remarks,
                        pricing=cart_item.pricing)
        shipment.save()
        ship_trxn = InventoryTransactions(
            trxn_type=4,
            ship=shipment,
            weight=cart_item.weight,
            trxn_user=user
        )
        ship_trxn.save()
        cart_item.delete()
    
    package.basic_amount = round((package.basic_rate * basic_weight),2)
    package.color_amount = round((package.color_rate * color_weight),2)
    package.wcut_amount = round((package.wcut_rate * wcut_weight),2)
    package.basic_weight = basic_weight
    package.color_weight = color_weight
    package.wcut_weight = wcut_weight

    package.print_amount = package.print_unit * package.print_rate
    package.block_amount = package.block_unit * package.block_rate

    package.total_amount = package.basic_amount + package.color_amount + \
                            package.wcut_amount + package.block_amount + \
                            package.print_amount + package.fare_amount - \
    package.save()
    return True


def get_packing_slip(package_id):
    package = PackingSlips.objects.get(pk=package_id)
    shippments = Ship.objects.filter(package=package) 
    ps_no = 'SPC/' + (5 - (len(str(package_id)))) * '0' + str(package_id)
    currency_symbol = u"\u20B9"
    context_dict = {
        'package': package,
        'shippments': shippments,
        'ps_no': ps_no,
        'currency_symbol': currency_symbol,
        'basic_rate': '{:0,.2f}'.format(package.basic_rate),
        'color_rate': '{:0,.2f}'.format(package.color_rate),
        'wcut_rate': '{:0,.2f}'.format(package.wcut_rate),
        'basic_amount': '{:0,.2f}'.format(package.basic_amount),
        'color_amount': '{:0,.2f}'.format(package.color_amount),
        'wcut_weight': '{:0,.2f}'.format(package.wcut_weight),
        'print_amount': '{:0,.2f}'.format(package.print_amount),
        'block_amount': '{:0,.2f}'.format(package.block_amount),
        'fare_amount': '{:0,.2f}'.format(package.fare_amount),
        'advance_amount': '{:0,.2f}'.format(package.advance_amount),
        'total_amount': '{:0,.2f}'.format(package.total_amount),
        'payable': '{:0,.0f}'.format(round((package.total_amount - package.advance_amount),0)),
    }
    template = get_template('packing_slip2.html')
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
    

        

        


    

