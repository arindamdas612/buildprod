from django.urls import path
from .views import seller, delete_seller, update_seller

urlpatterns = [
    path('', seller, name='sellers'),
    path('delete/<int:seller_id>', delete_seller, name='delete_seller'),
    path('update', update_seller, name='update_seller'),
]