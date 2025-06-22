from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from contest_platform.problem_repository import get_connection
from contest_platform.evaluator import evaluate_submission
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('task_list'))
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/tasks', methods=['GET'])
def task_list():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT problem_id, title FROM Problems')
    problems = cursor.fetchall()
    connection.close()
    return render_template('task_list.html', problems=problems)

@app.route('/task/<int:problem_id>', methods=['GET'])
def task_submission_page(problem_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT title, description FROM Problems WHERE problem_id = ?', (problem_id,))
    problem = cursor.fetchone()
    connection.close()
    if not problem:
        return 'Problem not found', 404
    return render_template('task_submission.html', problem_id=problem_id, title=problem[0], description=problem[1])

@app.route('/submit/<int:problem_id>', methods=['POST'])
def submit_code(problem_id):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    code = request.form.get('code')
    language = request.form.get('language', 'python')
    user_id = session['user_id']
    data = {
        'user_id': user_id,
        'problem_id': problem_id,
        'code': code,
        'language': language
    }
    result = evaluate_submission(data)
    return render_template('task_submission.html', problem_id=problem_id, title=request.form.get('title'), description=request.form.get('description'), result=result, code=code)

@app.route('/problem/create_problem', methods=['POST'])
def create_problem():
    data = request.json
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO Problems (title, description, time_limit, memory_limit)
    VALUES (?, ?, ?, ?)
    ''', (data['title'], data['description'], data['time_limit'], data['memory_limit']))

    problem_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return jsonify({"message": "Problem created", "problem_id": problem_id})

@app.route('/problem/add_test_case', methods=['POST'])
def add_test_case():
    data = request.json
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO TestCases (problem_id, input_data, expected_output)
    VALUES (?, ?, ?)
    ''', (data['problem_id'], data['input_data'], data['expected_output']))

    connection.commit()
    connection.close()

    return jsonify({"message": "Test case added"})

@app.route('/problem/list', methods=['GET'])
def list_problems():
    title_filter = request.args.get('filter')
    connection = get_connection()
    cursor = connection.cursor()

    if title_filter:
        cursor.execute("SELECT * FROM Problems WHERE title LIKE ?", (f"%{title_filter}%",))
    else:
        cursor.execute("SELECT * FROM Problems")

    problems = cursor.fetchall()
    connection.close()

    return jsonify([{
        "problem_id": p[0],
        "title": p[1],
        "description": p[2],
        "time_limit": p[3],
        "memory_limit": p[4]
    } for p in problems])

@app.route('/user/submit', methods=['POST'])
def submit_solution():
    data = request.json
    result = evaluate_submission(data)
    return jsonify(result)

@app.route('/user/submissions_list', methods=['GET'])
def list_submissions():
    user_id = request.args.get('user_id')
    problem_id = request.args.get('problem_id')

    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM Submissions"
    params = []

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    if problem_id:
        query += " AND problem_id = ?"
        params.append(problem_id)

    cursor.execute(query, params)
    submissions = cursor.fetchall()
    connection.close()

    return jsonify([{
        "submission_id": s[0],
        "user_id": s[1],
        "problem_id": s[2],
        "code": s[3],
        "language": s[4],
        "timestamp": s[5],
        "verdict": s[6]
    } for s in submissions])

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.json if request.is_json else request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        if request.is_json:
            return jsonify({'error': 'Missing fields'}), 400
        else:
            return render_template('register.html', error='Missing fields')

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('''
        INSERT INTO Users (username, email, password_hash)
        VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        connection.commit()
        user_id = cursor.lastrowid
        session['user_id'] = user_id
        if request.is_json:
            return jsonify({'message': 'User registered', 'user_id': user_id})
        else:
            return redirect(url_for('task_list'))
    except Exception as e:
        if request.is_json:
            return jsonify({'error': str(e)}), 400
        else:
            return render_template('register.html', error=str(e))
    finally:
        connection.close()

@app.route('/user/login', methods=['POST'])
def login_user():
    data = request.json if request.is_json else request.form
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing fields'}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    SELECT user_id, password_hash FROM Users WHERE username = ?
    ''', (username,))
    user = cursor.fetchone()
    connection.close()
    if user and user[1] == password_hash:
        session['user_id'] = user[0]
        if request.is_json:
            return jsonify({'message': 'Login successful', 'user_id': user[0]})
        else:
            return redirect(url_for('task_list'))
    else:
        if request.is_json:
            return jsonify({'error': 'Invalid username or password'}), 401
        else:
            return render_template('login.html', error='Invalid username or password')

def get_app():
    return app

if __name__ == "__main__":
    app.run(debug=True)