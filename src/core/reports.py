import datetime
import io
import xlsxwriter

from django.utils.timezone import get_current_timezone

from django.db.models import Sum, Count
from xlsxwriter.workbook import Workbook

from factory.models import Roll, InventoryTransactions


def get_report_dates():
    all_trxns = InventoryTransactions.objects.all()

    month_choice = []

    for trxn in all_trxns:
        ts = trxn.trxn_timestamp
        ts = ts.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        month_choice.append(ts.strftime('%b-%Y'))
    
    month_choice = list(set(month_choice))

    return month_choice

def get_report_data(period):
    data = []

    month_list = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    month, year = period.split('-')
    month = month_list[month]
    year = int(year)
    
    begin_date = datetime.datetime(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=get_current_timezone())
    
    next_month = month + 1
    if next_month > 12:
        next_month = 1
        year = year + 1
    end_date = begin_date.replace(month=next_month, year=year)
    end_date = end_date - datetime.timedelta(milliseconds=1)

    inward_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=0). \
        order_by('-roll__roll_type', 'trxn_timestamp')
    inward = []
    sl_no = 1
    for trxn in inward_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['type'] = trxn.roll.roll_type
        row['product'] = trxn.roll.color + ' ' + str(trxn.roll.gsm) + 'GSM ' + str(round(trxn.roll.width)) + '"'
        row['width'] = trxn.roll.width
        row['weight'] = trxn.weight
        row['length'] = trxn.roll.length
        inward.append(row)
        sl_no = sl_no + 1 

    production_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=1). \
        order_by('-bag__roll__roll_type', 'trxn_timestamp')
    production = []
    sl_no = 1

    for trxn in production_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['type'] = trxn.bag.roll.roll_type
        row['product'] = trxn.bag.roll.color + ' ' + str(trxn.bag.roll.gsm) + 'GSM ' + str(round(trxn.bag.roll.width)) + '"'
        row['width'] = trxn.bag.roll.width
        row['weight'] = trxn.weight
        row['unit'] = trxn.unit
        production.append(row)
        sl_no = sl_no + 1 

    
    outward_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=4). \
        order_by('-ship__bag__roll__roll_type', 'trxn_timestamp')
    outward = []
    sl_no = 1

    for trxn in outward_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['type'] = trxn.ship.bag.roll.roll_type
        row['product'] = trxn.ship.bag.roll.color + ' ' + str(trxn.ship.bag.roll.gsm) + 'GSM ' + str(round(trxn.ship.bag.roll.width)) + '"'
        row['width'] = trxn.ship.bag.roll.width
        row['weight'] = trxn.weight
        row['unit'] = trxn.unit
        outward.append(row)
        sl_no = sl_no + 1 

    stock_qs = Roll.objects.values('color', 'gsm', 'width', 'roll_type'). \
        annotate(total_units=Count('id')).order_by('roll_type', '-total_units')
    stock = []
    sl_no = 1
    for trxn in stock_qs:
        row = {}
        row['sl_no'] = sl_no
        row['type'] = trxn['roll_type']
        row['product'] = trxn['color'] + ' ' + str(trxn['gsm']) + 'GSM ' + str(round(trxn['width'])) + '"'
        row['width'] = trxn['width']
        row['unit'] = trxn['total_units']
        stock.append(row)
        sl_no = sl_no + 1 

    data.append(inward)
    data.append(production)
    data.append(outward)
    data.append(stock)

    return data


def get_report(data):

    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    
    header_format = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    body_format_1 = workbook.add_format({
        'bg_color': 'white',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    body_format_2 = workbook.add_format({
        'bg_color': 'white',
        'color': 'black',
        'align': 'right',
        'valign': 'top',
        'border': 1
    })

    # TAB - 1
    inward_sheet = workbook.add_worksheet('Inward Log')
    inward_data = data[0]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Date',
        'Type',
        'Product',
        'Width (inch)',
        'Weight (Kg)',
        'Length (m)'
    ]
    for header in header_column:
        inward_sheet.write(cur_row, header_column.index(header) , header, header_format)
    cur_row=+1
    #report body
    for row in inward_data:
        inward_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        inward_sheet.write(cur_row,  1, row['date'], body_format_1)
        inward_sheet.write(cur_row,  2, row['type'] + '-cut',body_format_1)
        inward_sheet.write(cur_row,  3, row['product'],body_format_1)
        inward_sheet.write(cur_row,  4, row['width'],body_format_2)
        inward_sheet.write(cur_row,  5, row['weight'], body_format_2)
        inward_sheet.write(cur_row,  6, row['length'], body_format_2)
        cur_row = cur_row + 1

    # TAB - 2
    production_sheet = workbook.add_worksheet('Production Log')
    production_data = data[1]
    cur_row = 0
    # header section
    for header in header_column:
        production_sheet.write(cur_row, header_column.index(header) , header, header_format)
    cur_row=+1
    #report body
    for row in production_data:
        production_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        production_sheet.write(cur_row,  1, row['date'], body_format_1)
        production_sheet.write(cur_row,  2, row['type'] + '-cut',body_format_1)
        production_sheet.write(cur_row,  3, row['product'],body_format_1)
        production_sheet.write(cur_row,  4, row['width'],body_format_2)
        production_sheet.write(cur_row,  5, row['weight'], body_format_2)
        production_sheet.write(cur_row,  6, row['unit'], body_format_2)
        cur_row = cur_row + 1


    # TAB - 3
    outward_sheet = workbook.add_worksheet('Outward Log')
    outward_data = data[2]
    cur_row = 0
    # header section
    for header in header_column:
        outward_sheet.write(cur_row, header_column.index(header) , header, header_format)
    cur_row=+1
    #report body
    for row in outward_data:
        outward_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        outward_sheet.write(cur_row,  1, row['date'], body_format_1)
        outward_sheet.write(cur_row,  2, row['type'] + '-cut',body_format_1)
        outward_sheet.write(cur_row,  3, row['product'],body_format_1)
        outward_sheet.write(cur_row,  4, row['width'],body_format_2)
        outward_sheet.write(cur_row,  5, row['weight'], body_format_2)
        outward_sheet.write(cur_row,  6, row['unit'], body_format_2)
        cur_row = cur_row + 1

    # TAB - 4
    stock_sheet = workbook.add_worksheet('Current Stock')
    stock_data = data[3]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Type',
        'Product',
        'Width (inch)',
        'Unit'
    ]
    for header in header_column:
        stock_sheet.write(cur_row, header_column.index(header) , header, header_format)
    cur_row=+1
    #report body
    for row in stock_data:
        stock_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        stock_sheet.write(cur_row,  1, row['type'] + '-cut',body_format_1)
        stock_sheet.write(cur_row,  2, row['product'],body_format_1)
        stock_sheet.write(cur_row,  3, row['width'],body_format_2)
        stock_sheet.write(cur_row,  4, row['unit'], body_format_2)
        cur_row = cur_row + 1




    workbook.close()

    output.seek(0)
    
    return output



