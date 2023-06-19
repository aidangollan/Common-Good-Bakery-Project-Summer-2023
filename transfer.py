from flask import Blueprint, render_template
from flask_login import login_required

transfer = Blueprint('transfer', __name__)

@transfer.route('/')
@login_required
def index():
    return render_template('transfer.html')

@transfer.route('/add_transfer')
@login_required
def add_transfer():
    return render_template('add_transfer.html')

@transfer.route('/view_transfers')
@login_required
def view_transfers():
    return render_template('view_transfers.html')