from django.urls import path
from .views import staff, delete_staff, status_staff

urlpatterns = [
    path('', staff, name='staffs'),
    path('delete/<int:staff_id>', delete_staff, name='staff_delete'),
    path('status/<int:staff_id>', status_staff, name='staff_status'),
]