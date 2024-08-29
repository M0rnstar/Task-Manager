from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db, User
from forms import RegistrationForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://task_user:4092manage4092@localhost/taskmanagement'
app.config['SECRET_KEY'] = 'ht!4ioy3*890uGDS@03KJ&'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("sign-in.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('sign-in'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
