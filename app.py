from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Task_Manager:40_manage_92@localhost/taskmanagement'
app.config['SECRET_KEY'] = 'ht!4ioy3*890uGDS@03KJ&'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("sign-in.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegistrationForm
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        return redirect(url_for('sign-in'))
    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
