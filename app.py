from flask import Flask, render_template, request, redirect, session, url_for
import database  

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong random string!

@app.route('/')
def bio():
    return render_template('bio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # You'll plug in a real login check here using database.py
        username = request.form['username']
        password = request.form['password']
        user = database.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            return redirect('/tasks')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    result = database.register_user(username, password)
    if result == "exists":
        return render_template('login.html', error="User already exists")
    return redirect('/login')

@app.route('/task')
def task_page():
    if 'user_id' not in session:
        return redirect('/login')
    tasks = database.get_tasks_by_user(session['user_id'])
    return render_template('task.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' in session:
        task_description = request.form['task']
        database.add_task(session['user_id'], task_description)
    return redirect('/task')

@app.route('/edit_task', methods=['POST'])
def edit_task():
    if 'user_id' in session:
        task_id = request.form['task_id']
        new_description = request.form['task']
        database.edit_task(session['user_id'], task_id, new_description)
    return redirect('/task')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    if 'user_id' in session:
        task_id = request.form['task_id']
        database.delete_task(session['user_id'], task_id)
    return redirect('/task')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)