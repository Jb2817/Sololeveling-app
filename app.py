from flask import Flask, render_template, request, redirect, url_for, session
from user import User, Task

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        user = User(name)
        session['user'] = user.__dict__
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/assign_tasks', methods=['POST'])
def assign_tasks():
    user = User(**session['user'])
    tasks = user.assign_tasks()
    session['user'] = user.__dict__
    session['tasks'] = [task.__dict__ for task in tasks]
    return redirect(url_for('index'))

@app.route('/update_progress', methods=['POST'])
def update_progress():
    user = User(**session['user'])
    tasks = [Task(**task) for task in session['tasks']]
    task_number = int(request.form['task_number'])
    value = int(request.form['value'])
    tasks[task_number - 1].update_progress(value)
    session['tasks'] = [task.__dict__ for task in tasks]
    if user.complete_tasks(tasks):
        user.level_up()
        tasks = user.assign_tasks()
        session['tasks'] = [task.__dict__ for task in tasks]
    session['user'] = user.__dict__
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
