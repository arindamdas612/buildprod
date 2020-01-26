from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import get_current_timezone
from django.db.models import Sum, Count
from django.http import HttpResponse

from core.models import Avatar
from .forms import RollForm, BagForm, ShipCartForm, PackingSlipForm, FlexoPrintForm, OffsetPrintForm
from .models import Waste, Roll, Bag, Ship, InventoryTransactions, ShipCart, PackingSlips
from .utils import waste_management, ship_package,get_packing_slip
from core.reports import get_report_dates

# Create your views here.
@login_required
def stock(request):
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    msg = ''
    if request.method == 'POST':
        form = RollForm(request.POST)
        if form.is_valid():
            new_roll = form.save()
            trxn = InventoryTransactions(
                trxn_type = 0,
                roll = new_roll,
                weight =  new_roll.weight,
                unit=new_roll.unit,
                trxn_user=request.user
            )
            trxn.save()
            msg = 'Roll stocked into inventory'
    template_name = 'stock.html'
    form = RollForm()
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Factory | Stock',
        'section_title': 'Stock Rolls',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'form': form,
        'msg': msg,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context)


@login_required
def make(request):
    make_form = BagForm()

    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    msg = ''
    if request.method == 'POST':
        roll_weight = float(request.POST.get('roll_weight'))
        waste_weight = float(request.POST.get('waste_weight'))
        roll = Roll.objects.get(pk=request.POST.get('roll_id'))
        make_form = BagForm(request.POST, roll_weight=roll_weight, waste_weight=waste_weight, roll=roll)
        if make_form.is_valid():
            bag = make_form.save()
            bag.status = 'stocked'
            bag.save()
            waste_management(bag.id, bag.roll.id, request.user, roll_weight, waste_weight)
            msg = 'Bag created and stocked into inventory!!!'
            make_form = BagForm()
        else:
            print(make_form.errors)
    rolls = Roll.objects.filter(unit__gt = 0, weight__gt=0).order_by('color', 'gsm', 'width', 'weight')
    template_name = 'make.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Factory | Make',
        'section_title': 'Make Bags',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'make_form': make_form,
        'msg': msg,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
        'rolls': rolls,
    }
    return render(request, template_name, context=context) 


@login_required
def ship(request):
    form = ShipCartForm(request.POST or None)
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    if request.method == 'POST':
        bag = Bag.objects.get(pk=request.POST['bag_id'])
        form = ShipCartForm(request.POST, bag=bag)
        if form.is_valid():
            cart_item = form.save(user=user)
            cart_bag = cart_item.bag
            cart_bag.status = 'in cart'
            cart_bag.save()
            form = ShipCartForm()

    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    template_name = 'ship.html'
    month_choice = get_report_dates()
    bags = Bag.objects.filter(weight__gt=0, status='stocked')
    context = {
        'title': 'Factory | Catalogue',
        'section_title': 'Shipping Cart',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        'form': form,
        'user_cart': user_cart,
        'cart_count': cart_count,
        'bags': bags
    }
    return render(request, template_name, context=context) 

@login_required
def delete_ship_cart(request, cart_id):
    if cart_id == 0:
        cart_items = ShipCart.objects.filter(cart_owner=request.user)
        for item in cart_items:
            bag = item.bag
            bag.status = 'stocked'
            bag.save()
            item.delete()
    else:
        cart_item = ShipCart.objects.get(pk=cart_id)
        bag = cart_item.bag
        bag.status = 'stocked'
        bag.save()
        cart_item.delete()
    
    return redirect('ship_bag')


@login_required
def price_shipments(request):
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    form = PackingSlipForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            cart_count = ShipCart.objects.filter(cart_owner=user).count()
            if cart_count > 0:
                package = form.save(user)
                ship_package(ps_id=package.id, user=user)
                
                pdf = get_packing_slip(package.id)
                if pdf:
                    ps_no = 'SPC/' + (5 - (len(str(package.id)))) * '0' + str(package.id)
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "PS_%s.pdf" %(ps_no)
                    content = "attachment; filename=%s" %(filename)
                    response['Content-Disposition'] = content
                    return response
            form = PackingSlipForm()

    basic_weight = 0
    basic_items = ShipCart.objects.filter(pricing='basic', cart_owner=user)
    for basic_item in basic_items:
        basic_weight+=basic_item.weight
    
    color_weight = 0
    color_items = ShipCart.objects.filter(pricing='colour', cart_owner=user)
    for color_item in color_items:
        color_weight+=color_item.weight
    
    wcut_weight = 0
    wcut_items = ShipCart.objects.filter(pricing='w-cut', cart_owner=user)
    for wcut_item in wcut_items:
        wcut_weight+=wcut_item.weight
    

    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    template_name = 'shipment_pricing.html'
    month_choice = get_report_dates()
    context = {
        'title': 'Factory | Pricing',
        'section_title': 'Shipment Pricing',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
        'basic_weight': basic_weight,
        'color_weight': color_weight,
        'wcut_weight': wcut_weight,
        'form': form,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 



@login_required
def package_history(request):
    packages = PackingSlips.objects.all().order_by('-create_timestamp')
    package_list = []
    
    for package in packages:
        temp_dict = {}
        temp_dict['id'] = package.id
        temp_dict['create_date'] = package.create_timestamp
        temp_dict['ps_no'] = 'SPC/' + (5 - (len(str(package.id)))) * '0' + str(package.id)
        temp_dict['party_name'] = package.party.name
        temp_dict['package_weight'] = package.color_weight + package.basic_weight
        temp_dict['package_value'] = '{:0,.2f}'.format(package.total_amount + package.advance_amount)
        package_list.append(temp_dict)
        
    
    paginator = Paginator(package_list, 20)
    page = request.GET.get('page')
    packages = paginator.get_page(page)
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'packages.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Factory | Package',
        'section_title': 'Package History',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,

        'packages': packages,
    }
    return render(request, template_name, context=context)

@login_required
def download_packingslip(request, package_id):
    package = PackingSlips.objects.get(pk=package_id)
    pdf = get_packing_slip(package.id)
    if pdf:
        ps_no = 'SPC/' + (5 - (len(str(package.id)))) * '0' + str(package.id)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "PS_%s.pdf" %(ps_no)
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response


@login_required
def flexo_print(request):
    rolls = Roll.objects.filter(unit__gt=0, print_type='Normal').order_by('color', 'width')
    form = FlexoPrintForm(request.POST or None)
    if request.method == 'POST':
        roll = Roll.objects.get(pk=int(request.POST.get('roll_id')))
        form = FlexoPrintForm(request.POST, roll=roll)
        if form.is_valid():
            printed_roll = form.save()
            trxn = InventoryTransactions(
                trxn_type = 5,
                roll = printed_roll,
                weight =  printed_roll.weight,
                unit=printed_roll.unit,
                trxn_user=request.user
            )
            trxn.save()
            form = FlexoPrintForm()

    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'flexo_print.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Print | Flexo',
        'section_title': 'Flexo Print',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,

        'rolls': rolls,
        'form': form,
    }
    return render(request, template_name, context=context)


@login_required
def offset_print(request):
    bags = Bag.objects.filter(weight__gt=0, roll__print_type='Normal', print_type='Normal', status='stocked').order_by('roll__color')
    form = OffsetPrintForm(request.POST or None)
    if request.method == 'POST':
        bag = Bag.objects.get(pk=int(request.POST.get('bag_id')))
        form = OffsetPrintForm(request.POST, bag=bag)
        if form.is_valid():
            printed_bag = form.save()
            trxn = InventoryTransactions(
                trxn_type = 6,
                bag = printed_bag,
                weight =  printed_bag.weight,
                trxn_user=request.user
            )
            trxn.save()
            form = OffsetPrintForm()
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'offset_print.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Print | Offset',
        'section_title': 'Offset Print',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,

        'bags': bags,
        'form': form,
    }
    return render(request, template_name, context=context)


@login_required
def flexo_log(request):

    trxns_list = InventoryTransactions.objects.filter(trxn_type=5).order_by('-trxn_timestamp')
    paginator = Paginator(trxns_list, 10)
    page = request.GET.get('page')
    trxns = paginator.get_page(page)

    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    month_choice = get_report_dates()
    template_name = 'log_5.html'
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Print Log | Flexo',
        'section_title': 'Flexo Print Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns, 
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,

    }
    return render(request, template_name, context=context) 


@login_required
def offset_log(request):

    trxns_list = InventoryTransactions.objects.filter(trxn_type=6).order_by('-trxn_timestamp')
    paginator = Paginator(trxns_list, 10)
    page = request.GET.get('page')
    trxns = paginator.get_page(page)

    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    month_choice = get_report_dates()
    template_name = 'log_6.html'
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Print Log | Offset',
        'section_title': 'Offset Print Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns, 
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,

    }
    return render(request, template_name, context=context) 



@login_required
def roll_warehouse(request):
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    #ed = datetime.date.now(tz=get_current_timezone())
    #st = ed - datetime.timedelta(days=1)
    
    rolls_list = Roll.objects.values('color', 'gsm', 'width', 'length', 'print_type'). \
        annotate(total_units=Sum('unit')).order_by('-total_units')
    paginator = Paginator(rolls_list,10)
    page = request.GET.get('page')
    rolls = paginator.get_page(page)
    template_name = 'warehouse-roll.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Warehouse | Roll',
        'section_title': 'Rolls',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'rolls': rolls,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 


@login_required
def bag_warehouse(request):
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    bag_list = Bag.objects.filter(status='stocked', weight__gt=0).order_by('-create_timestamp')
    paginator = Paginator(bag_list, 10)
    page = request.GET.get('page')
    bags = paginator.get_page(page)
    
    
    template_name = 'warehouse-bag.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Warehouse | Bag',
        'section_title': 'Bags',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'bags': bags,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 


@login_required
def waste_warehouse(request):
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    waste_list = Waste.objects.all().order_by('-create_timestamp')
    paginator = Paginator(waste_list, 20)
    page = request.GET.get('page')
    wastes = paginator.get_page(page)
    
    month_choice = get_report_dates()
    template_name = 'warehouse-waste.html'
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Warehouse | Waste',
        'section_title': 'Wastes',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'wastes': wastes,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 
    

@login_required
def inward_log(request):

    trxns_list = InventoryTransactions.objects.filter(trxn_type=0).order_by('-trxn_timestamp')
    paginator = Paginator(trxns_list, 10)
    page = request.GET.get('page')
    trxns = paginator.get_page(page)

    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    month_choice = get_report_dates()
    template_name = 'log_0.html'
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Activity | Inward',
        'section_title': 'Inward Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns, 
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,

    }
    return render(request, template_name, context=context) 


@login_required
def production_log(request):

    trxns_list = InventoryTransactions.objects.filter(trxn_type=1).order_by('-trxn_timestamp')
    paginator = Paginator(trxns_list, 10)
    page = request.GET.get('page')
    trxns = paginator.get_page(page)
    
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'log_1.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Activity | Production',
        'section_title': 'Production Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 


@login_required
def outward_log(request):

    trxns_list = InventoryTransactions.objects.filter(trxn_type=4).order_by('-trxn_timestamp')
    paginator = Paginator(trxns_list, 10)
    page = request.GET.get('page')
    trxns = paginator.get_page(page)
    
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'log_4.html'
    month_choice  = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Activity | Outward',
        'section_title': 'Outward Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 


@login_required
def waste_log(request):

    trxns_list = InventoryTransactions.objects.filter(trxn_type=2).order_by('-trxn_timestamp')
    paginator = Paginator(trxns_list, 10)
    page = request.GET.get('page')
    trxns = paginator.get_page(page)
    
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'log_2.html'
    month_choice = get_report_dates()
    user_cart = ShipCart.objects.filter(cart_owner=user)
    cart_count = ShipCart.objects.filter(cart_owner=user).count()
    context = {
        'title': 'Activity | Waste',
        'section_title': 'Waste Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns,
        'month_choice': month_choice,
        'user_cart': user_cart,
        'cart_count': cart_count,
    }
    return render(request, template_name, context=context) 
