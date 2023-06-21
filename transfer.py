from flask import Blueprint, render_template, redirect, request, jsonify
from flask_mail import Message
from flask_login import login_required
import json
from init import mail

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
        transfers = json.loads(transfers)

        for t in transfers:
            # Save transfers to the database here
            pass
            
        return jsonify({'success': True}), 200

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