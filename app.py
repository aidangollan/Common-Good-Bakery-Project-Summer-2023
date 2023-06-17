from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from db import db
from data_handling import Category, update_db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'some-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/')
def home():
    update_db(db)
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_fields = []
    error_message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error_fields.append('username')
        if not password:
            error_fields.append('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.form.get('next')
            if not next_page:
                abort(400, description="Missing next parameter for redirection after login")
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

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    return render_template('transfer.html')

@app.route('/add_transfer', methods=['GET', 'POST'])
@login_required
def add_transfer():
    return render_template('add_transfer.html')

@app.route('/view_transfers', methods=['GET', 'POST'])
@login_required
def view_transfers():
    return render_template('view_transfers.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)