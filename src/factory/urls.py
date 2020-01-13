from django.urls import path
from .views import stock, make, ship, delete_ship_cart, price_shipments, package_history, download_packingslip
from .views import flexo_print, offset_print
from .views import roll_warehouse, bag_warehouse, waste_warehouse
from .views import inward_log, production_log, outward_log, waste_log

from django.views.generic import TemplateView
urlpatterns = [
    path('stock/', stock, name='roll_stock'),
    path('make/', make, name='make_bag'),
    path('ship/', ship, name='ship_bag'),
    path('ship/delete/<int:cart_id>', delete_ship_cart, name='delete_ship_cart'),
    path('shippments/pricing', price_shipments, name='price_shipments'),
    path('package/history', package_history, name='package_history'),
    path('package/download/<int:package_id>', download_packingslip, name='download_packingslip'),
    path('print/flexo', flexo_print, name='flexo_print'),
    path('print/offset', offset_print, name='offset_print'),
    path('warehouse-rolls/', roll_warehouse, name='roll_activites'),
    path('warehoue-bags/', bag_warehouse, name='bag_activites'),
    path('warehouse-wastes/', waste_warehouse, name='waste_activites'),
    path('log-inward/', inward_log, name='inward_log'),
    path('log-production/', production_log, name='production_log'),
    path('log-outward/', outward_log, name='outward_log'),
    path('log-waste/', waste_log, name='waste_log'),
    path('color-seletor/', TemplateView.as_view(template_name="color_selector.html"), name="color-guide"),
    
]