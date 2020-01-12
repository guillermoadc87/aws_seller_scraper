import os
import sys
import csv
from math import ceil

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
                'tittle': row['Title'],
                'weekly_sell_avg': weekly_sell_avg if weekly_sell_avg > 0 else 0,
                'needed_quantity': needed_inventory,
            }

    with open(al) as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter='\t')
        for row in spamreader:
            #print(row)
            sku = [value for key, value in row.items() if 'seller-sku' in key][0]
            item = data.get(sku)
            if item:
                item['quantity'] = int(row['quantity'])
                item['status'] = row['status']

    with open(csv_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['tittle', 'weekly_sell_avg', 'status', 'quantity', 'needed_quantity'])
        writer.writeheader()
        for sku, item in data.items():
            print(item)
            if item['needed_quantity'] >= item['quantity']:
                writer.writerow(item)

    return data

if __name__ == '__main__':
    get_data()