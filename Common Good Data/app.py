from flask import Flask, render_template, request
from datetime import datetime
from main import load_menu, main, plot_graph
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

@app.route('/', methods=['GET', 'POST'])
def home():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    pickle_path = os.path.join(script_dir, 'menu.pickle')
    #main()
    menu = load_menu(pickle_path)
    categories = menu.get_all_categories()
    locations = menu.get_all_locations()

    plot_div = None
    if request.method == 'POST':
        chart_option = request.form.get('graph_type')
        category_option = request.form.get('category_option')
        location_option = request.form.get('location_option')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        selected_categories = request.form.getlist('category')
        selected_locations = request.form.getlist('location')

        start_date_dt = datetime.strptime(start_date, "%m/%d/%Y")
        end_date_dt = datetime.strptime(end_date, "%m/%d/%Y")

        plot_div = plot_graph(menu, chart_option, start_date_dt, end_date_dt, selected_categories, selected_locations, category_option, location_option)

    return render_template('index.html', plot_div=plot_div, categories=categories, locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
