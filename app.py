from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from init import db, mail
from models import User
import logging
from transfer import transfer as transfer_blueprint
from data_handling import Category, update_db

def add_user():
    hashed_password = bcrypt.generate_password_hash("aaa").decode('utf-8')
    user = User(username="aidan", password=hashed_password)
    db.session.add(user)
    db.session.commit()

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = 'some-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'commongoodmailer@gmail.com'
app.config['MAIL_PASSWORD'] = 'ezzfpkdadxsodorv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'

db.init_app(app)
mail.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    #add_user()
    update_db(db)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_fields = []
    error_message = None
    if request.method == 'POST':
        next_page = request.form.get('next')
        if current_user.is_authenticated:
            if not next_page:
                next_page = url_for('home')
            return redirect(next_page)
        username = request.form['username']
        password = request.form['password']

        if not username:
            error_fields.append('username')
        if not password:
            error_fields.append('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            if not next_page:
                next_page = url_for('home')
            return redirect(next_page)
        else:
            error_message = 'Login Unsuccessful. Please check username and password'

    return render_template('login.html', error_fields=error_fields, error_message=error_message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    # Fetch categories from the database
    categories = Category.query.with_entities(Category.name).distinct().all()
    categories = [category[0] for category in categories]
    locations = Category.query.with_entities(Category.location).distinct().all()
    locations = [location[0] for location in locations]

    return render_template('data.html', categories=categories, locations=locations)

# Register the transfer blueprint
app.register_blueprint(transfer_blueprint, url_prefix='/transfer')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)