from django.urls import path
from .views import dashboard, profile, update_password, update_avatar, DashboardChart, report_download

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('profile', profile, name='my_profile'),
    path('change_password', update_password, name='password_chg'),
    path('avatar_update', update_avatar, name='avatar_update'),
    path('api/chart-data', DashboardChart.as_view(), name='api-chart-data'),
    path('downlaod-report', report_download, name='report')
]
