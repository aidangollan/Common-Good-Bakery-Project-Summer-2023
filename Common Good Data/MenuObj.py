import itertools
from util import to_float
from datetime import datetime
from util import get_date_and_location

class Menu:
    def __init__(self):
        self.locations = {}

    def handle_file(self, file):
        date_info, location_info = get_date_and_location(file)

        file = itertools.dropwhile(lambda line: "Sales Categories" not in line, file)
        next(file, None)

        self.handle_location(location_info)

        self.locations[location_info].add_date(file, date_info)  # Pass datetime instead of string

    def handle_location(self, name):
        if name not in self.locations:
            location = Location(name)
            self.locations[name] = location

    def get_all_categories(self):
        categories = set()
        for location in self.locations.values():
            for date in location.dates.values():
                categories.update(date.keys())
        return sorted(list(categories))  
    
    def get_all_locations(self):
        return list(self.locations.keys()) 

    def is_date_valid(self, date):
        first_location = next(iter(self.locations.values()))
        return date in first_location.dates

    def is_date_range_valid(self, start_date, end_date):
        return self.is_date_valid(start_date) and self.is_date_valid(end_date)

    def get_date_range(self, start_date, end_date):
        first_location = next(iter(self.locations.values()))
        return sorted([date for date in first_location.dates if start_date <= date <= end_date])

    def get_sorted_location_names(self):
        return sorted(self.locations.keys())

    def get_categories(self, date):
        categories = set()
        for location in self.locations.values():
            categories.update(location.dates[date].keys())
        return sorted(list(categories))

class Location:
    def __init__(self, name):
        self.name = name
        self.dates = {}

    def add_date(self, file, date):
        categories = {}
        for line in file:
            line = line.strip()
            list_line = line.split(",")
        
            if list_line[1] == "Total":
                break

            if list_line[0] == "":
                category_name = list_line[1]
                categories[category_name] = Category(list_line[2:])
        
        self.dates[date] = categories  # date is now a datetime object

class Location:
    def __init__(self, name):
        self.name = name
        self.dates = {}

    def add_date(self, file, date):
        categories = {}
        for line in file:
            line = line.strip()
            list_line = line.split(",")
        
            if list_line[1] == "Total":
                break

            if list_line[0] == "":
                category_name = list_line[1]
                categories[category_name] = Category(list_line[2:])
        
        self.dates[date] = categories  # date is now a datetime object

class Category:
    def __init__(self, data):
        self.order_count = to_float(data[0])
        self.item_count = to_float(data[1])
        self.gross_amt = to_float(data[2])
        self.discounts = to_float(data[3])
        self.net = to_float(data[4])
        self.tax = to_float(data[5])
