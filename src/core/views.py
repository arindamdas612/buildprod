from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .models import Avatar
from factory.models import InventoryTransactions

from .analytics import get_weight_distribution
from .utils import get_chart0_data, get_chart1_data, get_chart2_data
from .reports import get_report_dates, get_report_data, get_report
# Create your views here.


@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    user = User.objects.get(username=request.user.username)
    avatar = Avatar.objects.get(user=user)
    tab_data = get_weight_distribution()
    month_choice = get_report_dates()
    context = {
        'title': 'Dashboard',
        'section_title': 'Dashboard',
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'admin_count': tab_data['admin_count'],
        'staff_count': tab_data['staff_count'],
        'seller_count': tab_data['seller_count'],
        'distributor_count': tab_data['distributor_count'],
        'stocked_weight': tab_data['stocked_weight'],
        'stock_percent': tab_data['stock_percent'],
        'outward_weight': tab_data['outward_weight'],
        'outward_percent': tab_data['outward_percent'],
        'waste_weight': tab_data['waste_weight'],
        'waste_percent': tab_data['waste_percent'],
        'month_choice': month_choice,
    }
    return render(request, template_name, context=context)


@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    has_error = False
    msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        if user.username != username:
            if len(username) > 0:
                usr = User.objects.filter(username=username).first()
                if usr:
                    has_error = True
                    msg = 'User Name already exist'
            else:
                has_error = True
                msg = 'User Name is required'
        
        if user.email != email:
            if len(email) > 0:
                usr = User.objects.filter(email=email).first()
                if usr:
                    has_error = True
                    msg = 'Email is taken exist'
            else:
                has_error = True
                msg = 'Email is required'
        
        if not has_error:
            if not (user.username == username and user.email == email and user.first_name == firstname and user.last_name == lastname):
                user.username = username
                user.email = email
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                msg = 'Profile Updated'
    user = User.objects.get(username=user.username)
    avatar = Avatar.objects.get(user=user)
    template_name = 'my_profile.html'
    month_choice = get_report_dates()
    context = {
        'title': 'Profile',
        'section_title': 'My Profile',
        'email': user.email,
        'username': user.username,
        'firstname': user.first_name,
        'lastname': user.last_name,
        'has_error': has_error,
        'message': msg,
        'avatar_path': 'img/profile_pics/'+ avatar.name + '.png',
        'month_choice': month_choice,
        
    }
    return render(request, template_name, context=context)


@login_required
def update_password(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        
        curr_password = request.POST.get('password_current')
        new_password = request.POST.get('password')
        cnf_password = request.POST.get('password1')

        if user.check_password(curr_password) and new_password == cnf_password:
            user.set_password(cnf_password)
            user.save()
    return redirect('my_profile')


@login_required
def update_avatar(request):
    if request.method == 'POST':
        avatar_name = request.POST.get('profile_avatar')
        if len(avatar_name) > 0:
            user = User.objects.get(id=request.user.id)
            avatar = Avatar.objects.get(user=user)
            avatar.name = avatar_name
            avatar.save()
    
    return redirect('my_profile')


@login_required
@staff_member_required
def report_download(request):
    if request.method == 'POST':
        report_period = request.POST.get('report-period')

        data = get_report_data(period=report_period)
        report_filename = report_period + '.xlsx'
        
        xlsx_data = get_report(data)

        response = HttpResponse(xlsx_data.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=" + report_filename

        return response

        
    return redirect('dashboard')



class DashboardChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        type_0 = get_chart0_data()
        type_1 = get_chart1_data()
        type_2 = get_chart2_data()


        return Response([type_0, type_1, type_2])





