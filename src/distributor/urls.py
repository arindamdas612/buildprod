from django.urls import path
from .views import distributor, delete_distributor, update_distributor

urlpatterns = [
    path('', distributor, name='distributors'),
    path('delete/<int:distributor_id>', delete_distributor, name='delete_distributor'),
    path('update', update_distributor, name='update_distributor'),
]