import datetime
import io
import xlsxwriter

from django.utils.timezone import get_current_timezone

from django.db.models import Sum, Count
from xlsxwriter.workbook import Workbook

from factory.models import Roll, Bag, InventoryTransactions


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
        order_by('trxn_timestamp')
    inward = []
    sl_no = 1
    for trxn in inward_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['product'] = trxn.roll.color + ' ' + str(trxn.roll.gsm) + ' GSM ' + str(round(trxn.roll.width)) + '"'
        row['gsm'] = trxn.roll.gsm
        row['width'] = trxn.roll.width
        row['weight'] = round(trxn.weight,2)
        row['length'] = trxn.roll.length
        inward.append(row)
        sl_no = sl_no + 1 

    production_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=1). \
        order_by('trxn_timestamp')
    production = []
    sl_no = 1

    for trxn in production_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['product'] = trxn.bag.roll.color + ' ' + str(trxn.bag.roll.gsm) + ' GSM'
        row['gsm'] = trxn.bag.roll.gsm
        row['type'] = trxn.bag.bag_type
        if trxn.bag.roll.print_type == 'Flexo':
            row['print'] = trxn.bag.roll.print_type
        else:
            row['print'] = trxn.bag.print_type
        row['size'] = str(round(trxn.bag.height)) + ' X ' + str(round(trxn.bag.width)) 
        row['weight'] = trxn.weight
        production.append(row)
        sl_no = sl_no + 1 
    
    
    outward_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=4). \
        order_by( 'trxn_timestamp')
    outward = []
    sl_no = 1

    for trxn in outward_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['product'] = trxn.ship.bag.roll.color + ' ' + str(trxn.ship.bag.roll.gsm) + ' GSM'
        row['gsm'] = trxn.ship.bag.roll.gsm
        row['type'] = trxn.ship.bag.bag_type
        if trxn.ship.bag.roll.print_type == 'Flexo':
            row['print'] = trxn.ship.bag.roll.print_type
        else:
            row['print'] = trxn.ship.bag.print_type
        row['size'] = str(round(trxn.ship.bag.height)) + ' X ' + str(round(trxn.ship.bag.width))
        row['weight'] = trxn.weight 
        outward.append(row)
        sl_no = sl_no + 1 
    
    flexo_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=5). \
        order_by( 'trxn_timestamp')
    flexo = []
    sl_no = 1

    for trxn in flexo_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['product'] = trxn.roll.color + ' ' + str(trxn.roll.gsm) + ' GSM ' + str(round(trxn.roll.width)) + '"'
        row['gsm'] = trxn.roll.gsm
        row['width'] = trxn.roll.width
        row['weight'] = round(trxn.weight,2)
        row['length'] = trxn.roll.length
        flexo.append(row)
        sl_no = sl_no + 1

    offset_qs = InventoryTransactions.objects. \
        filter(trxn_timestamp__lte=end_date,trxn_timestamp__gte=begin_date, trxn_type=6). \
        order_by('trxn_timestamp')
    offset = []
    sl_no = 1

    for trxn in offset_qs:
        row = {}
        row['sl_no'] = sl_no
        row['date'] = trxn.trxn_timestamp.strftime('%d.%m.%Y')
        row['product'] = trxn.bag.roll.color + ' ' + str(trxn.bag.roll.gsm) + ' GSM'
        row['gsm'] = trxn.bag.roll.gsm
        row['type'] = trxn.bag.bag_type
        row['size'] = str(round(trxn.bag.height)) + ' X ' + str(round(trxn.bag.width)) 
        row['weight'] = trxn.weight
        offset.append(row)
        sl_no = sl_no + 1 
     

    stock_roll_qs = Roll.objects.values('color', 'gsm', 'width', 'print_type'). \
        annotate(total_units=Sum('unit')).order_by('-total_units')
    stock = []
    sl_no = 1
    for trxn in stock_roll_qs:
        row = {}
        row['sl_no'] = sl_no
        row['product'] = trxn['color'] + ' ' + str(trxn['gsm']) + ' GSM ' + str(round(trxn['width'])) + '"'
        row['gsm'] = trxn['gsm']
        row['width'] = trxn['width']
        row['print_type'] = trxn['print_type']
        row['unit'] = trxn['total_units']
        stock.append(row)
        sl_no = sl_no + 1 
    
    stock_bag_qs = Bag.objects.values('roll__color', 'roll__gsm', 'bag_type', 'height', 'width', 'print_type', 'roll__print_type'). \
        annotate(total_weight=Sum('weight')).order_by('-total_weight')
    stock_bag = []
    sl_no = 1
    for trxn in stock_bag_qs:
        row = {}
        row['sl_no'] = sl_no
        row['product'] = trxn['roll__color'] + ' ' + str(trxn['roll__gsm']) + ' GSM'
        row['gsm'] = trxn['roll__gsm']
        row['size'] = str(round(trxn['height'])) + ' X ' + str(round(trxn['width']))
        row['type'] = trxn['bag_type']
        row['print'] =  trxn['roll__print_type'] if trxn['roll__print_type'] == 'Flexo' else trxn['print_type']
        row['weight'] = round(trxn['total_weight'],2)
        stock_bag.append(row)
        sl_no = sl_no + 1 

    data.append(inward)
    data.append(production)
    data.append(outward)
    data.append(flexo)
    data.append(offset)
    data.append(stock)
    data.append(stock_bag)

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
        'border': 1,
    })
    body_format_3 = workbook.add_format({
        'bg_color': 'white',
        'color': 'black',
        'align': 'right',
        'valign': 'top',
        'border': 1,
        'num_format': '#,##0.00'
    })

    # TAB - 1
    inward_sheet = workbook.add_worksheet('Inward Log')
    inward_data = data[0]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Date',
        'Product',
        'GSM',
        'Width (inch)',
        'Weight (Kg)',
        'Length (m)'
    ]
    header_width = [2, 10, 25, 3, 12, 11, 10]
    for header in header_column:
        col_num = header_column.index(header)
        inward_sheet.write(cur_row, header_column.index(header) , header, header_format)
        inward_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in inward_data:
        inward_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        inward_sheet.write(cur_row,  1, row['date'], body_format_1)
        inward_sheet.write(cur_row,  2, row['product'],body_format_1)
        inward_sheet.write(cur_row,  3, row['gsm'],body_format_1)
        inward_sheet.write(cur_row,  4, row['width'],body_format_2)
        inward_sheet.write(cur_row,  5, row['weight'], body_format_3)
        inward_sheet.write(cur_row,  6, row['length'], body_format_2)
        cur_row = cur_row + 1
    


    # TAB - 2
    production_sheet = workbook.add_worksheet('Production Log')
    production_data = data[1]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Date',
        'Product',
        'GSM',
        'Bag Type',
        'Print',
        'Size (inch)',
        'Weight (Kg)',
    ]
    header_width = [2, 10, 25, 4, 20, 20, 15, 11]
    for header in header_column:
        col_num = header_column.index(header)
        production_sheet.write(cur_row, header_column.index(header) , header, header_format)
        production_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in production_data:
        production_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        production_sheet.write(cur_row,  1, row['date'], body_format_1)
        production_sheet.write(cur_row,  2, row['product'],body_format_1)
        production_sheet.write(cur_row,  3, row['gsm'],body_format_1)
        production_sheet.write(cur_row,  4, row['type'], body_format_1)
        production_sheet.write(cur_row,  5, row['print'], body_format_1)
        production_sheet.write(cur_row,  6, row['size'],body_format_1)
        production_sheet.write(cur_row,  7, row['weight'], body_format_3)
        cur_row = cur_row + 1


    # TAB - 3
    outward_sheet = workbook.add_worksheet('Outward Log')
    outward_data = data[2]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Date',
        'Product',
        'GSM',
        'Bag Type',
        'Print',
        'Size (inch)',
        'Weight (Kg)',
    ]
    header_width = [2, 10, 25, 4, 20, 20, 15, 11]
    for header in header_column:
        col_num = header_column.index(header)
        outward_sheet.write(cur_row, header_column.index(header) , header, header_format)
        outward_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in outward_data:
        outward_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        outward_sheet.write(cur_row,  1, row['date'], body_format_1)
        outward_sheet.write(cur_row,  2, row['product'],body_format_1)
        outward_sheet.write(cur_row,  3, row['gsm'],body_format_1)
        outward_sheet.write(cur_row,  4, row['type'],body_format_1)
        outward_sheet.write(cur_row,  5, row['print'],body_format_1)
        outward_sheet.write(cur_row,  6, row['size'],body_format_1)
        outward_sheet.write(cur_row,  7, round(row['weight'],2), body_format_3)
        cur_row = cur_row + 1


    # TAB - 4
    flexo_sheet = workbook.add_worksheet('Flexo Print Log')
    flexo_data = data[3]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Date',
        'Product',
        'GSM',
        'Width (inch)',
        'Weight (Kg)',
        'Length (m)'
    ]
    header_width = [2, 10, 25, 3, 12, 11, 10]
    for header in header_column:
        col_num = header_column.index(header)
        flexo_sheet.write(cur_row, header_column.index(header) , header, header_format)
        flexo_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in flexo_data:
        flexo_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        flexo_sheet.write(cur_row,  1, row['date'], body_format_1)
        flexo_sheet.write(cur_row,  2, row['product'],body_format_1)
        flexo_sheet.write(cur_row,  3, row['gsm'],body_format_1)
        flexo_sheet.write(cur_row,  4, row['width'],body_format_2)
        flexo_sheet.write(cur_row,  5, row['weight'], body_format_3)
        flexo_sheet.write(cur_row,  6, row['length'], body_format_2)
        cur_row = cur_row + 1

    # TAB - 5
    offset_sheet = workbook.add_worksheet('Offset Print Log')
    offset_data = data[4]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Date',
        'Product',
        'GSM',
        'Bag Type',
        'Size (inch)',
        'Weight (Kg)',
    ]
    header_width = [2, 10, 25, 4, 20, 15, 11]
    for header in header_column:
        col_num = header_column.index(header)
        offset_sheet.write(cur_row, header_column.index(header) , header, header_format)
        offset_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in offset_data:
        offset_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        offset_sheet.write(cur_row,  1, row['date'], body_format_1)
        offset_sheet.write(cur_row,  2, row['product'],body_format_1)
        offset_sheet.write(cur_row,  3, row['gsm'],body_format_1)
        offset_sheet.write(cur_row,  4, row['type'], body_format_1)
        offset_sheet.write(cur_row,  5, row['size'],body_format_1)
        offset_sheet.write(cur_row,  6, row['weight'], body_format_3)
        cur_row = cur_row + 1

    # TAB - 6
    stock_sheet = workbook.add_worksheet('Stock - Roll')
    stock_data = data[5]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Product',
        'GSM',
        'Width (inch)',
        'Print Type',
        'Unit'
    ]
    header_width = [2, 25, 4, 20, 20, 11]
    for header in header_column:
        col_num = header_column.index(header)
        stock_sheet.write(cur_row, header_column.index(header) , header, header_format)
        outward_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in stock_data:
        stock_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        stock_sheet.write(cur_row,  1, row['product'],body_format_1)
        stock_sheet.write(cur_row,  2, row['gsm'],body_format_1)
        stock_sheet.write(cur_row,  3, row['width'],body_format_2)
        stock_sheet.write(cur_row,  4, row['print_type'],body_format_1)
        stock_sheet.write(cur_row,  5, row['unit'], body_format_2)
        cur_row = cur_row + 1
    
    # TAB - 7
    stock_bag_sheet = workbook.add_worksheet('Stock - Bag')
    stock_bag_data = data[6]
    cur_row = 0
    # header section
    header_column = [
        '#',
        'Product',
        'GSM',
        'Size (inch)',
        'Bag Type',
        'Print',
        'Weight (Kg)'
    ]
    header_width = [2, 25, 4, 15, 10, 15, 15]
    for header in header_column:
        col_num = header_column.index(header)
        stock_bag_sheet.write(cur_row, header_column.index(header) , header, header_format)
        stock_bag_sheet.set_column(col_num, 1, header_width[col_num])
    cur_row=+1
    #report body
    for row in stock_bag_data:
        stock_bag_sheet.write(cur_row,  0, row['sl_no'], body_format_2)
        stock_bag_sheet.write(cur_row,  1, row['product'],body_format_1)
        stock_bag_sheet.write(cur_row,  2, row['gsm'],body_format_1)
        stock_bag_sheet.write(cur_row,  3, row['size'],body_format_1)
        stock_bag_sheet.write(cur_row,  4, row['type'], body_format_1)
        stock_bag_sheet.write(cur_row,  5, row['print'], body_format_1)
        stock_bag_sheet.write(cur_row,  6, row['weight'], body_format_3)
        cur_row = cur_row + 1


    workbook.close()
    output.seek(0)
    return output



