from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user
from models import db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://task_user:4092manage4092@localhost/taskmanagement'
app.config['SECRET_KEY'] = 'ht!4ioy3*890uGDS@03KJ&'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    print("Запрос получен")
    form = LoginForm()
    if form.validate_on_submit():
        print("Отправка произошла")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            print("Ты залогинился")
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print("Произошла какая-то ошибка")
    return render_template("login/index.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register/index.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html')


@app.route('/about')
@login_required
def about():
    return render_template('about/index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
