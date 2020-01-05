from django.shortcuts import render, redirect
from .models import Distributor
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from core.reports import get_report_dates

from core.models import Avatar

# Create your views here.

@login_required
def distributor(request):
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
            new_distributor = Distributor(name=name, contact=contact, email=email)
            new_distributor.save()
        
    distributor_list = Distributor.objects.all()
    paginator = Paginator(distributor_list,4)
    template_name = 'distributor.html'
    page = request.GET.get('page')
    distributors = paginator.get_page(page)
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    month_choice = get_report_dates()
    context = {
        'title': 'Parties',
        'section_title': 'Party - All',
        'distributors': distributors,
        'has_error': has_error,
        'msg': msg,
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
    }
    return render(request, template_name, context=context)


@login_required
@staff_member_required
def delete_distributor(requset, distributor_id):
    distributor = Distributor.objects.get(id=distributor_id)
    distributor.delete()
    return redirect('distributors')


@login_required
@staff_member_required
def update_distributor(request):
    if request.method == 'POST':
        has_error = False
        distributor_id = request.POST.get('distributor_id')
        name = request.POST.get('name')
        contact = request.POST.get('mobile')
        email = request.POST.get('email')
        if len(name) == 0:
            has_error = True
        else:
            if len(contact) == 0:
                has_error = True

        if not has_error:
            distributor = Distributor.objects.get(id=distributor_id)
            distributor.name=name
            distributor.contact=contact
            distributor.email=email
            distributor.save()
    
    return redirect('distributors')


