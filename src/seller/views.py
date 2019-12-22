from django.shortcuts import render, redirect
from .models import Seller
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from core.models import Avatar
from core.reports import get_report_dates

# Create your views here.

@login_required
def seller(request):
    has_error = False
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('mobile')
        email = request.POST.get('email')
        if len(name) == 0:
            has_error = True
            msg = 'Name is required'
        else:
            if len(contact) == 0:
                has_error = True
                msg = 'Mobile number is required'
        if not has_error:
            new_seller = Seller(name=name, contact=contact, email=email)
            new_seller.save()
        
    seller_list = Seller.objects.all()
    paginator = Paginator(seller_list,4)
    template_name = 'seller.html'
    page = request.GET.get('page')
    sellers = paginator.get_page(page)
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    month_choice = get_report_dates()
    context = {
        'title': 'Sellers',
        'section_title': 'Seller - All',
        'sellers': sellers,
        'has_error': has_error,
        'msg': msg,
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice
    }
    return render(request, template_name, context=context)


@login_required
@staff_member_required
def delete_seller(requset, seller_id):
    seller = Seller.objects.get(id=seller_id)
    seller.delete()
    return redirect('sellers')


@login_required
@staff_member_required
def update_seller(request):
    if request.method == 'POST':
        has_error = False
        seller_id = request.POST.get('seller_id')
        name = request.POST.get('name')
        contact = request.POST.get('mobile')
        email = request.POST.get('email')
        if len(name) == 0:
            has_error = True
        else:
            if len(contact) == 0:
                has_error = True

        if not has_error:
            seller = Seller.objects.get(id=seller_id)
            seller.name=name
            seller.contact=contact
            seller.email=email
            seller.save()
    
    return redirect('sellers')


