import os
import pickle
import shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # importing pandas
from datetime import datetime
from MenuObj import Menu
from MenuObj import Category

def main():
    menu = load_menu()

    folder = "daily files/unprocessed"

    for filename in os.listdir(folder):
        if filename.endswith(".xls"):  # checking if file is .xls
            xls_filepath = os.path.join(folder, filename)
            csv_filepath = xls_filepath.replace('.xls', '.csv')  # new csv filepath
            
            # convert xls to csv
            df = pd.read_excel(xls_filepath)
            df.to_csv(csv_filepath, index=False)

            filename = filename.replace('.xls', '.csv')  # update filename to csv
            filepath = os.path.join(folder, filename)  # update filepath to csv
            
            os.remove(xls_filepath)  # remove original xls file after conversion

        else:
            filepath = os.path.join(folder, filename)

        with open_file(filepath) as file:
            menu.handle_file(file)
        shutil.move(filepath, 'daily files/processed/' + filename)

    save_menu(menu)

def plot_graph(menu, graph_type, start_date=None, end_date=None, category=None):
    if graph_type == 'stacked_bar':
        plot_stacked_bar(menu, start_date)
    elif graph_type == 'stacked_line':
        if start_date is None or end_date is None or category is None:
            print("Error: Missing argument for stacked line graph")
        else:
            plot_stacked_line(menu, start_date, end_date, category)

def plot_stacked_line(menu, start_date, end_date, category):
    if not menu.is_date_range_valid(start_date, end_date):
        print("Error: Invalid date range")
        return

    dates = menu.get_date_range(start_date, end_date)
    location_names = menu.get_sorted_location_names()

    location_data = calculate_percent_contributions(menu, dates, location_names, category)

    plot_line_chart(dates, location_data, location_names, category)

def plot_stacked_bar(menu, date):
    if not menu.is_date_valid(date):
        print("Error: Invalid date")
        return

    categories = menu.get_categories(date)
    location_names = menu.get_sorted_location_names()

    location_data = calculate_percent_contributions_for_bar(menu, date, categories, location_names)

    plot_bar_chart(categories, location_data, location_names, date)

def calculate_percent_contributions(menu, dates, location_names, category):
    location_data = []

    for location_name in location_names:
        location = menu.locations[location_name]
        location_percent_contributions = []

        for date in dates:
            gross_amt = location.dates.get(date, {}).get(category, Category([0]*6)).gross_amt
            total_gross_amt = sum([loc.dates.get(date, {}).get(category, Category([0]*6)).gross_amt for loc in menu.locations.values()])
            percent_contribution = gross_amt / total_gross_amt * 100 if total_gross_amt != 0 else 0
            location_percent_contributions.append(percent_contribution)

        location_data.append(location_percent_contributions)

    return location_data

def calculate_percent_contributions_for_bar(menu, date, categories, location_names):
    total_gross_amounts = {category: 0 for category in categories}
    for location in menu.locations.values():
        for category in categories:
            total_gross_amounts[category] += location.dates.get(date, {}).get(category, Category([0]*6)).gross_amt

    location_data = []

    for location_name in location_names:
        location = menu.locations[location_name]
        gross_amounts = [location.dates.get(date, {}).get(category, Category([0]*6)).gross_amt for category in categories]
        percent_contributions = [gross_amt / total_gross_amounts[category] * 100 if total_gross_amounts[category] != 0 else 0 for gross_amt, category in zip(gross_amounts, categories)]
        location_data.append(percent_contributions)

    return location_data

def plot_line_chart(dates, location_data, location_names, category):
    plt.figure(figsize=(10,6))

    for i, percent_contributions in enumerate(location_data):
        plt.plot(dates, percent_contributions, label=location_names[i])

    plt.xlabel('Date')
    plt.ylabel('Percentage Contribution (%)')
    plt.title(f'Percentage Contribution by Date for {category} at Each Location')
    plt.legend()
    plt.tight_layout()

def plot_bar_chart(categories, location_data, location_names, date):
    bar_pos = np.arange(len(categories))

    plt.figure(figsize=(10,6))

    plt.bar(bar_pos, location_data[0], label=location_names[0])
    for i in range(1, len(location_names)):
        plt.bar(bar_pos, location_data[i], bottom=np.sum(location_data[:i], axis=0), label=location_names[i])

    plt.xlabel('Categories')
    plt.ylabel('Percentage Contribution (%)')
    plt.title(f'Percentage Contribution by Category for Each Location on {date}')
    plt.xticks(bar_pos, categories, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()

def open_file(name):
    return open(name,"r")

def load_menu():
    try:
        with open('menu.pickle', 'rb') as f:
            menu = pickle.load(f)
    except FileNotFoundError:
        menu = Menu()
    return menu

def save_menu(menu):
    with open('menu.pickle', 'wb') as f:
        pickle.dump(menu, f)

if __name__ == "__main__":
    main()