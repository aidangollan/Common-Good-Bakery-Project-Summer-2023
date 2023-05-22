import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request
import matplotlib.pyplot as plt, io, base64
from datetime import datetime
import pandas as pd
from main import plot_graph, load_menu, main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    main()
    menu = load_menu()

    # get all categories
    categories = menu.get_all_categories()

    if request.method == 'POST':
        graph_type = request.form.get('graph_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        category = request.form.get('category')

        # Convert dates to desired format
        start_date_dt = datetime.strptime(start_date, "%m/%d/%Y")
        end_date_dt = datetime.strptime(end_date, "%m/%d/%Y")

        if start_date_dt == end_date_dt:
            graph_type = 'stacked_bar'

        img = create_plot(menu, graph_type, start_date_dt, end_date_dt, category)
        return render_template('index.html', img=img, categories=categories, request=request)
    return render_template('index.html', img=None, categories=categories, request=request)

def create_plot(menu, graph_type, start_date=None, end_date=None, category=None):
    img = io.BytesIO()
    plot_graph(menu, graph_type, start_date, end_date, category)
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True)