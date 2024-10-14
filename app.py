from flask import Flask, render_template, url_for, redirect, flash, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Task
from forms import RegistrationForm, LoginForm, ResetForm
from datetime import timedelta

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://task_user:4092manage4092@localhost/taskmanagement'
app.config['SECRET_KEY'] = 'ht!4ioy3*890uGDS@03KJ&'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.config['SESSION_PERMANENT'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_page = request.args.get('next')
    print(next_page)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            remember_me = form.remember_me.data
            login_user(user, remember=remember_me)
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
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


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            print('Пароль закоммичен')
            return redirect(url_for('login'))
    return render_template('forgot_password/index.html', form=form)


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
    session.clear()
    response = redirect(url_for('login'))
    response.delete_cookie('remember_token')
    return response


@app.route('/api/add-task', methods=['POST'])
def add_task():
    task_data = request.json
    title = task_data.get('title')
    description = task_data.get('content')
    deadline = task_data.get('deadline')

    user = current_user
    if user is None:
        return jsonify({'message': 'Пользователь не авторизован'}), 401
    new_task = Task(title=title, description=description, deadline=deadline, user_id=user.id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Задача успешно добавлена', 'task': {'title': title, 'description': description, 'deadline': deadline}}), 201


@app.route('/api/get-tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'title': task.title,
            'content': task.description,
            'deadline': task.deadline,
            'id': task.id
        })
    return jsonify(tasks_list)

@app.route('/api/delete-task/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)

    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'})

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
