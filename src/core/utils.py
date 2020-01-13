from factory.models import InventoryTransactions, PackingSlips
import datetime

from django.utils.timezone import get_current_timezone
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth

def get_months():
    months = []

    st = datetime.datetime.now(tz=get_current_timezone())
    st = st.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    months.append(st)
    prev_month = st
    for i in range(0,5):
        mon = prev_month.month
        mon = mon - 1
        yr = prev_month.year
        if mon == 0:
            mon = 12
            yr = yr - 1
        
        prev_month = prev_month.replace(month=mon, year=yr)
        months.append(prev_month)
    
    months.sort()
    
    return months


def get_days(num):
    days = []
    st = datetime.datetime.now(tz=get_current_timezone())
    prev_day = st
    days.append(prev_day)
    for i in range(0,num+1):
        prev_day = prev_day - datetime.timedelta(days=1)
        days.append(prev_day)
    

    days.sort()
    return days


def get_chart0_data():
    type_0_labels = []
    type_0_stock = []
    type_0_production = []
    type_0_waste = []

    months = get_months()

    for month in months:
        type_0_labels.append(month.strftime('%b-%y'))

        st = month
        year = st.year
        next_month = st.month + 1

        if next_month > 12:
            next_month = 1
            year = year + 1

        ed = st.replace(month=next_month, year=year) - datetime.timedelta(days=1)

        stock_qs=InventoryTransactions.objects.  \
            annotate(month=TruncMonth('trxn_timestamp')). \
            values('month'). \
            filter(trxn_type=0,trxn_timestamp__lte=ed,trxn_timestamp__gte=st). \
            annotate(weight=Sum('weight'))

        if stock_qs:
            for trxn in stock_qs:
                type_0_stock.append(round(trxn['weight'],2))
        else:
            type_0_stock.append(0)

        production_qs=InventoryTransactions.objects.  \
            annotate(month=TruncMonth('trxn_timestamp')). \
            values('month'). \
            filter(trxn_type=1,trxn_timestamp__lte=ed,trxn_timestamp__gte=st). \
            annotate(weight=Sum('weight')) 

        if production_qs:
            for trxn in production_qs:
                type_0_production.append(round(trxn['weight'],2))  
        else:
            type_0_production.append(0)

        waste_qs=InventoryTransactions.objects.  \
            annotate(month=TruncMonth('trxn_timestamp')). \
            values('month'). \
            filter(trxn_type=2,trxn_timestamp__lte=ed,trxn_timestamp__gte=st). \
            annotate(weight=Sum('weight')) 

        if waste_qs:
            for trxn in waste_qs:
                type_0_waste.append(round(trxn['weight'],2)) 
        else:
            type_0_waste.append(0)
    
    type_0_data = [type_0_stock, type_0_production, type_0_waste]

    data = {
            'label': type_0_labels,
            'data': type_0_data
        }
    return data



def get_chart1_data():
    type_1_labels = []
    type_1_stock = []
    type_1_production = []
    type_1_waste = []

    days = get_days(5)

    for day in days:
        type_1_labels.append(day.strftime('%d/%m'))
        ed = day.replace(hour=23, minute=59, second=59, microsecond=0)
        st = ed.replace(hour=0, minute=0, second=0, microsecond=0)

        stock_qs=InventoryTransactions.objects.  \
            annotate(day=TruncDay('trxn_timestamp')). \
            values('day'). \
            filter(trxn_type=0,trxn_timestamp__lte=ed,trxn_timestamp__gte=st). \
            annotate(weight=Sum('weight'))

        if stock_qs:
            for trxn in stock_qs:
                type_1_stock.append(round(trxn['weight'],2))
        else:
            type_1_stock.append(0)

        production_qs=InventoryTransactions.objects.  \
            annotate(day=TruncDay('trxn_timestamp')). \
            values('day'). \
            filter(trxn_type=1,trxn_timestamp__lte=ed,trxn_timestamp__gte=st). \
            annotate(weight=Sum('weight')) 

        if production_qs:
            for trxn in production_qs:
                type_1_production.append(round(trxn['weight'],2))  
        else:
            type_1_production.append(0)

        waste_qs=InventoryTransactions.objects.  \
            annotate(day=TruncDay('trxn_timestamp')). \
            values('day'). \
            filter(trxn_type=2,trxn_timestamp__lte=ed,trxn_timestamp__gte=st). \
            annotate(weight=Sum('weight')) 

        if waste_qs:
            for trxn in waste_qs:
                type_1_waste.append(round(trxn['weight'],2)) 
        else:
            type_1_waste.append(0)
    
    type_1_data = [type_1_stock, type_1_production, type_1_waste]

    data = {
            'label': type_1_labels,
            'data': type_1_data
        }
    return data


def get_chart2_data():


    type_2_color = []
    type_2_label = []
    type_2_data = []
    rolls_stocked = InventoryTransactions.objects.values('roll__gsm', 'roll__width', 'roll__color') \
        .annotate(total_unit=Sum('weight')) \
        .filter(trxn_type=0) 

    bags_produced = InventoryTransactions.objects.values('bag__roll__gsm', 'bag__roll__width', 'bag__roll__color') \
        .annotate(total_unit=Sum('weight')) \
        .filter(trxn_type=1) 

    for roll in rolls_stocked:
        plot = {}

        plot['label'] = roll['roll__color'] + ' ' + str(roll['roll__gsm']) + 'GSM ' + str(roll['roll__width']) + "in"
        plot['backgroundColor'] = roll['roll__color']
        plot['hoverBackgroundColor'] = roll['roll__color']
        plot['hoverBorderColor'] = 'black'
        plot['hoverBorderWidth'] = 2

    
        data = {}

        data['x'] = round(roll['total_unit'])
        data['y'] = 0
        for bag in bags_produced:
            if bag['bag__roll__color'] == roll['roll__color'] and \
            bag['bag__roll__gsm'] == roll['roll__gsm'] and \
            bag['bag__roll__width'] == roll['roll__width']:
                data['y'] = round(bag['total_unit'])
        data['r'] = round(roll['roll__width']/4,2)

        plot['data'] = [data]

        type_2_data.append(plot)

    bags_produced = InventoryTransactions.objects.values('bag__roll__gsm', 'bag__roll__width', 'bag__roll__color') \
        .annotate(total_unit=Sum('unit')) \
        .filter(trxn_type=1) 

    
    data = {
        'data': type_2_data 
    }
    return data

def get_chart3_data():
    type_3_labels = []
    type_3_data = []

    days = get_days(8)
    for day in days:
        type_3_labels.append(day.strftime('%d/%m'))
        ed = day.replace(hour=23, minute=59, second=59, microsecond=0)
        st = ed.replace(hour=0, minute=0, second=0, microsecond=0)

        sales=PackingSlips.objects.  \
            annotate(day=TruncDay('create_timestamp')). \
            values('day'). \
            filter(create_timestamp__lte=ed,create_timestamp__gte=st). \
            annotate(amount=Sum('total_amount'))

        if sales:
            for trxn in sales:
                try: 
                    type_3_data.append(round(trxn['amount']))
                except:
                    type_3_data.append(0)
        else:
            type_3_data.append(0)
    
    data = {
            'label': type_3_labels,
            'data': type_3_data
        }
    return data
