from flask import Blueprint, render_template, redirect, request
from flask_mail import Message
from flask_login import login_required
from models import Transfer
from init import db, mail

transfer = Blueprint('transfer', __name__)

@transfer.route('/')
@login_required
def index():
    return render_template('transfer.html')

@transfer.route('/add_transfer', methods=['GET', 'POST'])
@login_required
def add_transfer():
    if request.method == 'POST':
        transfers = []
        i = 0
        while f'item{i}' in request.form:
            item = request.form.get(f'item{i}')
            location = request.form.get(f'location{i}')
            amount = request.form.get(f'amount{i}')
            date = request.form.get(f'date{i}')
            transfers.append(Transfer(item=item, location=location, amount=amount, date=date))
            i += 1

        db.session.add_all(transfers)
        db.session.commit()

        return 'success', 200

    return render_template('add_transfer.html')

@transfer.route('/view_transfers')
@login_required
def view_transfers():
    return render_template('view_transfers.html')

@transfer.route('/send_transfer', methods=['POST'])
@login_required
def send_transfer():
    msg = Message('Transfer Notification', sender = 'commongoodmailer@gmail.com', recipients = ['aidangollan@icloud.com'])
    msg.body = "A transfer has been sent"
    mail.send(msg)
    return redirect('/transfer')