from db import db
from util import to_float, to_int
from datetime import datetime
import os

PROCESSED_FILES = 'processed_files.txt'
CSV_FILES_DIR = os.path.join(os.path.dirname(__file__), 'csv_files')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    order_count = db.Column(db.Integer, nullable=False)
    item_count = db.Column(db.Integer, nullable=False)
    gross_amt = db.Column(db.Integer, nullable=False)
    discounts = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    def __init__(self, location, date, name, order_count, item_count, gross_amt, discounts, net, tax):
        self.location = location
        self.date = date
        self.name = name
        self.order_count = order_count
        self.item_count = item_count
        self.gross_amt = gross_amt
        self.discounts = discounts
        self.net = net
        self.tax = tax

def update_db(db):
    processed_files = load_processed_files()
    for file_name in os.listdir(CSV_FILES_DIR):
        if file_name not in PROCESSED_FILES:
            file_path = os.path.join(CSV_FILES_DIR, file_name)
            with open(file_path, 'r') as file:
                categories = process_file(file)
            # Update the list of processed files
            processed_files.append(file_name)
            save_processed_files(processed_files)
        for category in categories:
            db.session.add(category)
    db.session.commit()

def process_file(file):
    categories = []
    skip = True
    break_check = False
    lines = file.readlines()

    date = lines[1].split(',')[0].split(' ')[0]

    if lines[1].split(',')[-2].split(' ')[2] == 'Bakery':
        location = lines[1].split(',')[-2].split(' ')[-2] + ' ' + lines[1].split(',')[-2].split(' ')[-1]
    else:
        location = lines[1].split(',')[-2]
    
    for line in lines:
        line = line.split(',')
        if line[0] == 'Sales Categories':
            break_check = True
            skip = False
            continue
        if line[1] == 'Total' and break_check:
            break
        if skip:
            continue        
        name = line[1]
        order_count = to_int(line[2])
        item_count = to_int(line[3])
        gross_amt = to_int(line[4])
        discounts = to_float(line[5])
        net = to_float(line[6])
        tax = to_float(line[7])
        categories.append(Category(location, date, name, order_count, 
                        item_count, gross_amt, discounts, net, tax))
    return categories

def get_date_and_location(file):
    next(file, None)
    line = next(file).strip()
    list_line = line.split(",")
    date_list = list_line[0].split(" - ")
    date_info = date_list[0]
    
    # Convert date_info to a datetime object
    date_info_dt = datetime.strptime(date_info, "%m/%d/%y")

    location_list = list_line[-2].split(" - ")
    location_info = location_list[-1]
    return date_info_dt, location_info

def load_processed_files():
    # Use relative path for processed files
    processed_files_path = os.path.join(os.path.dirname(__file__), PROCESSED_FILES)
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as f:
            return f.read().splitlines()
    else:
        return []

def save_processed_files(files):
    # Use relative path for processed files
    processed_files_path = os.path.join(os.path.dirname(__file__), PROCESSED_FILES)
    with open(processed_files_path, 'w') as f:
        for file in files:
            f.write(f"{file}\n")