import datetime

from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.functions import TruncDay 
from django.utils.timezone import get_current_timezone

from factory.models import Bag, Roll, Waste, Ship, InventoryTransactions
from seller.models import Seller
from distributor.models import Distributor

def get_weight_distribution():
    data = dict()

    st = datetime.datetime.now(tz=get_current_timezone())
    st = st.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    next_month = st.month + 1
    next_year = st.year
    if next_month > 12:
        next_month = next_month - 12
        next_year = next_year + 1
    ed = st.replace(month=next_month, year=next_year) - datetime.timedelta(days=1)


    stocked_weight = InventoryTransactions.objects.filter(trxn_timestamp__lte=ed,trxn_timestamp__gte=st, trxn_type=0).aggregate(Sum('weight'))
    used_stock_weight = InventoryTransactions.objects.filter(trxn_timestamp__lte=ed,trxn_timestamp__gte=st, trxn_type=3).aggregate(Sum('weight'))
    produce_weight = InventoryTransactions.objects.filter(trxn_timestamp__lte=ed,trxn_timestamp__gte=st, trxn_type=1).aggregate(Sum('weight'))
    outward_weight = InventoryTransactions.objects.filter(trxn_timestamp__lte=ed,trxn_timestamp__gte=st, trxn_type=4).aggregate(Sum('weight'))
    waste_weight = InventoryTransactions.objects.filter(trxn_timestamp__lte=ed,trxn_timestamp__gte=st, trxn_type=2).aggregate(Sum('weight'))
    
    stocked_weight = stocked_weight['weight__sum']
    used_stock_weight = used_stock_weight['weight__sum']
    produce_weight = produce_weight['weight__sum']
    outward_weight = outward_weight['weight__sum']
    waste_weight = waste_weight['weight__sum']

    data['seller_count'] = Seller.objects.all().count()
    data['distributor_count'] = Distributor.objects.all().count()
    data['admin_count'] = User.objects.filter(is_staff=True).count()
    data['staff_count'] = User.objects.filter(is_staff=False).count()
    
    if stocked_weight > 0:
        data['stocked_weight'] = round(stocked_weight/1000,1)
    else:
        data['stocked_weight'] = 0

    try:
        data['stock_percent'] = round((used_stock_weight/stocked_weight) * 100)
    except:
        data['stock_percent'] = 0
    
    if outward_weight:
        data['outward_weight'] = round(outward_weight/1000,1)
    else:
        data['outward_weight'] = 0
    
    try:
        data['outward_percent'] = round((outward_weight/produce_weight) * 100)
    except:
        data['outward_percent'] = 0

    if waste_weight:
        data['waste_weight'] = round(waste_weight/1000, 1)
    else:
        data['waste_weight'] = 0
    try:
        data['waste_percent'] = round((waste_weight/used_stock_weight) * 100)
    except:
        data['waste_percent'] = 0

    return data






    


        
