from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from core.reports import get_report_dates
import re

from core.models import Avatar

# Create your views here.

@login_required
@staff_member_required
def staff(request):
    has_error = False
    regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    msg = "all valid"
    # post request to handle new staff creation
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')

        if(re.search(regex_email,email)):
            user = User.objects.filter(email=email).first()
            if user:
                msg = 'The Email is taken'
                has_error = True
            else:
                if len(username) < 0:
                    msg = 'UserName is required'
                    has_error = True
                else:
                    user = User.objects.filter(username=username).first()
                    if user:
                        msg = 'The username is taken'
                        has_error = True
        else:
            msg = "Invalid Email"
            has_error = True
        
        if not has_error:
            user = User.objects.create_user(username=username, password='1111', email=email, first_name=firstname, last_name=lastname, is_active=False)
            avatar = Avatar(user=user)
            avatar.save()


    template_name = 'staff.html'
    
    staff_list = User.objects.filter(is_staff=False)
    paginator = Paginator(staff_list,4)

    page = request.GET.get('page')
    staffs = paginator.get_page(page)
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    month_choice = get_report_dates()
    context = {
        'title': 'Staffs',
        'section_title': 'Staff - All',
        'staffs': staffs,
        'has_error': has_error,
        'msg': msg,
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice
    }
    return render(request, template_name, context=context)


@login_required
@staff_member_required
def delete_staff(requset, staff_id):
    staff = User.objects.get(id=staff_id)
    staff.delete()
    return redirect('staffs')


@login_required
@staff_member_required
def status_staff(requset, staff_id):
    staff = User.objects.get(id=staff_id)
    staff.is_active = not staff.is_active
    staff.save()
    return redirect('staffs')
