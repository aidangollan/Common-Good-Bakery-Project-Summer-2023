from flask import Blueprint, render_template, redirect, request, jsonify
from flask_mail import Message
from flask_login import login_required
from models import Transfer
from datetime import datetime
import json
import logging
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
        transfers = request.form.get('transfers')
        print(f"Transfers: {transfers}")
        transfers = json.loads(transfers)

        for t in transfers:
            date = datetime.strptime(t['date'], '%m/%d/%y')
            new_transfer = Transfer(item=t['item'], location=t['location'], amount=t['amount'], date=date)
            db.session.add(new_transfer)
        db.session.commit()
        send_transfer()
        return redirect('/transfer')

    return render_template('add_transfer.html')

@transfer.route('/view_transfers')
@login_required
def view_transfers():
    return render_template('view_transfers.html')

def send_transfer():
    msg = Message('Transfer Notification', sender = 'commongoodmailer@gmail.com', recipients = ['aidangollan@icloud.com'])
    msg.body = "A transfer has been sent"
    mail.send(msg)