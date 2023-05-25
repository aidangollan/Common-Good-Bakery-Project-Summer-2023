import os
import pickle
import shutil
import plotly.graph_objs as go
from plotly.graph_objs import Pie
import pandas as pd
from datetime import datetime
from MenuObj import Menu
from MenuObj import Category
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import os

def main():
    menu = load_menu()

    script_dir = os.path.dirname(os.path.realpath(__file__))  # get the directory of this script
    unprocessed_folder = os.path.join(script_dir, "daily files/unprocessed")  # get the unprocessed folder path
    processed_folder = os.path.join(script_dir, "daily files/processed")  # get the processed folder path

    for filename in os.listdir(unprocessed_folder):
        if filename.endswith(".xls"):  # checking if file is .xls
            xls_filepath = os.path.join(unprocessed_folder, filename)
            csv_filepath = xls_filepath.replace('.xls', '.csv')  # new csv filepath
            
            # convert xls to csv
            df = pd.read_excel(xls_filepath)
            df.to_csv(csv_filepath, index=False)

            filename = filename.replace('.xls', '.csv')  # update filename to csv
            filepath = os.path.join(unprocessed_folder, filename)  # update filepath to csv
            
            os.remove(xls_filepath)  # remove original xls file after conversion

        else:
            filepath = os.path.join(unprocessed_folder, filename)

        with open_file(filepath) as file:
            menu.handle_file(file)

        shutil.move(filepath, os.path.join(processed_folder, filename))

    save_menu(menu)

def plot_graph(menu, chart_option, start_date, end_date, categories, locations, category_option, location_option):
    if not menu.is_date_range_valid(start_date, end_date):
        print("Error: Invalid date range")
        return
    dates = menu.get_date_range(start_date, end_date)
    category_data = calculate_percent_contributions(menu, dates, categories, "category", locations)
    location_data = calculate_percent_contributions(menu, dates, locations, "location", categories)
    if category_option.strip('_')[0] != location_option.strip('_')[0]:
        if chart_option == 'line_chart':
            if category_option == "aggregate_categories":
                return plot_line_chart(dates, categories, locations, location_data, None)
            else:
                return plot_line_chart(dates, categories, locations, None, category_data)
        elif chart_option == 'pie_chart':
            if category_option == "aggregate_categories":
                return plot_pie_chart(categories, locations, location_data, None)
            else:
                return plot_pie_chart(categories, locations, None, category_data)

def plot_pie_chart(categories, locations, location_data, category_data):
    if location_data != None:
        location_data_aggregate = aggregate_pie_data(location_data)
        data = plot_pie_data(locations, location_data_aggregate)
        layout = make_layout(categories, "Categories", "Location")
    else:
        category_data_aggregate = aggregate_pie_data(category_data)
        data = plot_pie_data(categories, category_data_aggregate)
        layout = make_layout(locations, "Locations", "Category")

    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)

    return plot_div

def aggregate_pie_data(data):
    data_out = []
    for list in data:
        data_out.append(sum(list) / len(list))
    return [data_out]

def plot_line_chart(dates, categories, locations, location_data, category_data):
    if location_data != None:
        data = make_line_data(dates, locations, location_data)
        layout = make_layout(categories, "Categories", "Location")
    else:
        data = make_line_data(dates, categories, category_data)
        layout = make_layout(locations, "Locations", "Category")

    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)

    return plot_div

def plot_pie_data(names, values):
    data = []
    for i in range(len(values)):
        trace = Pie(
            labels = names,
            values = values[i],
            name = f'Date {i}'
        )
        data.append(trace)
    return data

def make_line_data(dates, categories, category_data):
    data = []
    for i in range(len(categories)):
        trace = go.Scatter(
            x = dates,
            y = category_data[i],
            mode = 'lines',
            name = categories[i]
        )
        data.append(trace)
    
    return data

def make_layout(names, data_name, key_name):
    return go.Layout(
        title = f'Percentage Contribution by Date for {len(names)} {data_name} at Each {key_name}',
        xaxis = dict(title = 'Date'),
        yaxis = dict(title = 'Percentage Contribution (%)'),
    )

def calculate_percent_contributions(menu, dates, base_items, base_item_type, cross_items):
    cross_item_data = []

    for base_item in base_items:
        base_item_contributions = []
        for date in dates:
            gross_amt = sum_gross_amt(menu, date, base_item, base_item_type, cross_items)
            total_gross_amt = sum([sum_gross_amt(menu, date, item, base_item_type, cross_items) for item in base_items])
            percent_contribution = gross_amt / total_gross_amt * 100 if total_gross_amt != 0 else 0
            base_item_contributions.append(percent_contribution)
        cross_item_data.append(base_item_contributions)

    return cross_item_data

def sum_gross_amt(menu, date, base_item, base_item_type, cross_items):
    if base_item_type == "location":
        location = menu.locations.get(base_item)
        if location:
            return sum([location.dates.get(date, {}).get(cross_item, Category([0]*6)).gross_amt for cross_item in cross_items])
    elif base_item_type == "category":
        return sum([menu.locations[loc].dates.get(date, {}).get(base_item, Category([0]*6)).gross_amt for loc in cross_items])

    return 0

def open_file(name):
    return open(name,"r")

def load_menu():
    menu_file = os.path.join(BASE_DIR, 'menu.pickle')
    try:
        with open(menu_file, 'rb') as f:
            menu = pickle.load(f)
    except FileNotFoundError:
        menu = Menu()
    return menu

def save_menu(menu):
    menu_file = os.path.join(BASE_DIR, 'menu.pickle')
    with open(menu_file, 'wb') as f:
        pickle.dump(menu, f)

if __name__ == "__main__":
    main()
