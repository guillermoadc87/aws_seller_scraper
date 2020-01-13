import os
import sys
import csv
from math import ceil
from openpyxl import load_workbook

number_of_weeks = 12
csv_filename = "out_of_stock.csv"
lead_times = {
    'fire-lite': 4,
    'notifier': 4,
    'simplex': 8,
    'edwards': 4,
    'system sensor': 4,
    'potter': 4,
    'siemens': 7,
    'bosh': 4,
    'vesda': 3,
    'lenel': 4,
    'mircom': 4,
    'fci gamewell': 4
}

headers = [
    'Item',
    'SKU',
    'Status',
    'Weekly Sell AVG',
    'Inventory Needed',
    'Total Inventory',
    'Quaitity On Hand',
    'Quaitity On Purchase Order',
]

def get_lead_time(title):
    lead_time = 4
    for key in lead_times:
        if key in title:
            lead_time = lead_times[key]
    return lead_time

def get_filename_with_extension(ext):
    """
    Looks for a file with the pass extension

    :String:
    """
    filename = [f for f in os.listdir() if ext in f]

    if filename:
        return filename[0]

    return False

def get_data():
    data = {}

    br = get_filename_with_extension('csv')
    qb = get_filename_with_extension('xlsx')
    al = get_filename_with_extension('txt')

    if not br or not al:
        sys.exit(1)

    with open(br) as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            weekly_sell_avg = ceil(int(row['Units Ordered'])/number_of_weeks)
            daily_avg = ceil(weekly_sell_avg/5)

            needed_inventory = ceil(weekly_sell_avg * get_lead_time(row['Title']))
            data[row['SKU']] = {
                'Item': row['Title'],
                'SKU': row['SKU'],
                'Status': '',
                'Weekly Sell AVG': weekly_sell_avg if weekly_sell_avg > 0 else 0,
                'Inventory Needed': needed_inventory,
                'Total Inventory': 0,
                'Quaitity On Hand': 0,
                'Quaitity On Purchase Order': 0,
            }

    wb = load_workbook(filename=qb)

    ws = wb['Sheet1']

    for row in ws.rows:
        sku = row[2].value
        qoh = row[4].value
        qopo = row[5].value
        if sku and qoh is not None and qopo is not None:
            item = data.get(sku)
            if item:
                item['Total Inventory'] = qoh + qopo
                item['Quaitity On Hand'] = qoh
                item['Quaitity On Purchase Order'] = qopo

    with open(al) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter='\t')
        for row in spamreader:
            #print(row)
            sku = [value for key, value in row.items() if 'seller-sku' in key][0]
            item = data.get(sku)
            if item:
                #item['quantity'] = int(row['quantity'])
                item['Status'] = row['status']

    with open(csv_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for sku, item in data.items():
            if item['Inventory Needed'] >= item['Total Inventory']:
                writer.writerow(item)

    return data

if __name__ == '__main__':
    get_data()