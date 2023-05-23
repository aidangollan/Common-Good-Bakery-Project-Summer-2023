import os
import pickle
import shutil
import plotly.graph_objs as go
import pandas as pd
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

def plot_graph(menu, start_date=None, end_date=None, categories=None, locations=None):
    # handles different types of graphs
    if not menu.is_date_range_valid(start_date, end_date):
        print("Error: Invalid date range")
        return
    
    if len(categories) == 1:
        return plot_line_chart_multi_location(menu, start_date, end_date, locations, categories[0])
    else:
        return plot_line_chart_multi_category(menu, start_date, end_date, locations[0], categories)
        
def plot_line_chart_multi_location(menu, start_date, end_date, locations, category):
    dates = menu.get_date_range(start_date, end_date)
    location_data = calculate_percent_contributions_multi_location(menu, dates, locations, category)

    data = []
    for i in range(len(locations)):
        trace = go.Scatter(
            x = dates,
            y = location_data[i],
            mode = 'lines',
            name = locations[i]
        )
        data.append(trace)

    layout = go.Layout(
        title = f'Percentage Contribution by Date for {category} at Each Location',
        xaxis = dict(title = 'Date'),
        yaxis = dict(title = 'Percentage Contribution (%)'),
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)

    return plot_div

def plot_line_chart_multi_category(menu, start_date, end_date, location, categories):
    dates = menu.get_date_range(start_date, end_date)
    category_data = calculate_percent_contributions_multi_category(menu, dates, location, categories)

    data = []
    for i in range(len(categories)):
        trace = go.Scatter(
            x = dates,
            y = category_data[i],
            mode = 'lines',
            name = categories[i]
        )
        data.append(trace)

    layout = go.Layout(
        title = f'Percentage Contribution by Date at {location} for each Category',
        xaxis = dict(title = 'Date'),
        yaxis = dict(title = 'Percentage Contribution (%)'),
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)

    return plot_div

def calculate_percent_contributions_multi_location(menu, dates, locations, category):
    location_data = []

    for location_name in locations:
        location = menu.locations.get(location_name)
        location_percent_contributions = []
        if location is not None:
            for date in dates:
                gross_amt = location.dates.get(date, {}).get(category, Category([0]*6)).gross_amt
                total_gross_amt = sum([loc.dates.get(date, {}).get(category, Category([0]*6)).gross_amt for loc in menu.locations.values()])
                percent_contribution = gross_amt / total_gross_amt * 100 if total_gross_amt != 0 else 0
                location_percent_contributions.append(percent_contribution)
            location_data.append(location_percent_contributions)
        else:
            location_data.append([0]*len(dates))  # no data for this location, so append zeroes

    return location_data

def calculate_percent_contributions_multi_category(menu, dates, location_name, categories):
    category_data = []
    location = menu.locations.get(location_name)
    if location is not None:
        for category in categories:
            category_percent_contributions = []
            for date in dates:
                gross_amt = location.dates.get(date, {}).get(category, Category([0]*6)).gross_amt
                total_gross_amt = sum([location.dates.get(date, {}).get(cat, Category([0]*6)).gross_amt for cat in categories])
                percent_contribution = gross_amt / total_gross_amt * 100 if total_gross_amt != 0 else 0
                category_percent_contributions.append(percent_contribution)
            category_data.append(category_percent_contributions)
    else:
        for _ in categories:
            category_data.append([0]*len(dates))  # no data for this location, so append zeroes for each category

    return category_data

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
