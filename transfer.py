from flask import Blueprint, render_template, request
from flask_mail import Message
from flask_login import login_required
from init import mail

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

@transfer.route('/send_transfer', methods=['POST'])
@login_required
def send_transfer():
    msg = Message('Transfer Notification', sender = 'your-email@gmail.com', recipients = ['specific-email@gmail.com'])
    msg.body = "A transfer has been sent"
    mail.send(msg)
    return 'Email sent'