from init import db
from datetime import datetime
from flask_login import UserMixin

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    order_count = db.Column(db.Integer, nullable=False)
    item_count = db.Column(db.Integer, nullable=False)
    gross_amt = db.Column(db.Integer, nullable=False)
    discounts = db.Column(db.Float, nullable=False)
    net = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    def __init__(self, location, date, name, order_count, item_count, gross_amt, discounts, net, tax):
        self.location = location
        self.date = date
        self.name = name
        self.order_count = order_count
        self.item_count = item_count
        self.gross_amt = gross_amt
        self.discounts = discounts
        self.net = net
        self.tax = tax

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    