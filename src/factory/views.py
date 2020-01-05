from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import get_current_timezone
from django.db.models import Sum, Count

from core.models import Avatar
from .forms import RollForm, BagForm, ShipForm, ShipCartForm
from .models import Waste, Roll, Bag, Ship, InventoryTransactions, ShipCart
from .utils import waste_management
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
    context = {
        'title': 'Factory | Stock',
        'section_title': 'Stock Rolls',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'form': form,
        'msg': msg,
        'month_choice': month_choice
    }
    return render(request, template_name, context=context)


@login_required
def make(request):
    make_form = BagForm()
    ship_form = ShipForm()

    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    msg = ''
    if request.method == 'POST':
        roll_weight = request.POST.get('roll_weight')
        waste_weight = request.POST.get('waste_weight')
        make_form = BagForm(request.POST, roll_weight=roll_weight, waste_weight=waste_weight)
        if make_form.is_valid():
            bag = make_form.save()
            waste_management(bag.id, bag.roll.id, request.user, roll_weight, waste_weight)
            msg = 'Bag created and stocked into inventory!!!'
            make_form = BagForm()
    template_name = 'make.html'
    month_choice = get_report_dates()
    context = {
        'title': 'Factory | Make',
        'section_title': 'Make Bags',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'make_form': make_form,
        'ship_form': ship_form,
        'msg': msg,
        'month_choice': month_choice
    }
    return render(request, template_name, context=context) 


@login_required
def ship(request):
    """
    if request.method == 'POST':
        form = ShipForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            shipment = form.save(request.user)
            shipped_bag = shipment.bag
            shipped_bag.status = 'SHIPPED'
            shipped_bag.save()

            ship_trxn = InventoryTransactions(
                trxn_type=4,
                ship=shipment,
                weight = shipped_bag.weight,
                unit=shipped_bag.unit,
                trxn_user = request.user
            )
            ship_trxn.save()
    
    return redirect('make_bag')
    """
    form = ShipCartForm(request.POST or None)
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    if request.method == 'POST':
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
    context = {
        'title': 'Factory | Ship',
        'section_title': 'Shipping Cart',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        'form': form,
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
    
    rolls_list = Roll.objects.values('color', 'gsm', 'width', 'length'). \
        annotate(total_units=Sum('unit')).order_by('-total_units')
    paginator = Paginator(rolls_list,10)
    page = request.GET.get('page')
    rolls = paginator.get_page(page)
    template_name = 'warehouse-roll.html'
    month_choice = get_report_dates()
    context = {
        'title': 'Warehouse | Roll',
        'section_title': 'Rolls',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'rolls': rolls,
        'month_choice': month_choice
    }
    return render(request, template_name, context=context) 


@login_required
def bag_warehouse(request):
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)

    bag_list = Bag.objects.filter(status='STOCKED').order_by('-create_timestamp')
    paginator = Paginator(bag_list, 20)
    page = request.GET.get('page')
    bags = paginator.get_page(page)
    
    
    template_name = 'warehouse-bag.html'
    month_choice = get_report_dates()
    context = {
        'title': 'Warehouse | Bag',
        'section_title': 'Bags',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'bags': bags,
        'month_choice': month_choice
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
    context = {
        'title': 'Warehouse | Waste',
        'section_title': 'Wastes',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'wastes': wastes,
        'month_choice': month_choice
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
    context = {
        'title': 'Activity | Inward',
        'section_title': 'Inward Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns, 
        'month_choice': month_choice
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
    context = {
        'title': 'Activity | Production',
        'section_title': 'Production Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns,
        'month_choice': month_choice
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
    context = {
        'title': 'Activity | Outward',
        'section_title': 'Outward Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns,
        'month_choice': month_choice
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
    context = {
        'title': 'Activity | Waste',
        'section_title': 'Waste Log',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'transactions': trxns,
        'month_choice': month_choice
    }
    return render(request, template_name, context=context) 
