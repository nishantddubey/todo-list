from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'your_secret_key'

# MongoDB connection
connection_string = 'mongodb://localhost:27017/'
client = MongoClient(connection_string)
db = client['todo_list']
users_collection = db['users']
tasks_collection = db['tasks']

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated

class User(UserMixin):
    def __init__(self, username, user_id):
        self.username = username
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user['username'], str(user['_id']))
    return None

@app.route('/')
@login_required
def index():
    tasks = {
        'pending': list(tasks_collection.find({'status': 'pending', 'user_id': current_user.id})),
        'ongoing': list(tasks_collection.find({'status': 'ongoing', 'user_id': current_user.id})),
        'completed': list(tasks_collection.find({'status': 'completed', 'user_id': current_user.id}))
    }
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    task = request.form.get('task')
    reminder = request.form.get('reminder')
    tasks_collection.insert_one({
        'task': task,
        'status': 'pending',  # Initial status
        'reminder': reminder if reminder else None,
        'user_id': current_user.id
    })
    return redirect(url_for('index'))

@app.route('/set_status/<task_id>/<status>')
@login_required
def set_status(task_id, status):
    if status in ['pending', 'ongoing', 'completed']:
        tasks_collection.update_one({'_id': ObjectId(task_id), 'user_id': current_user.id}, {'$set': {'status': status}})
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
@login_required
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id), 'user_id': current_user.id})
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users_collection.insert_one({'username': username, 'password': hashed_password})
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            login_user(User(username, str(user['_id'])))
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
