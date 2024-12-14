from flask import Flask, request, jsonify
from contest_platform.problem_repository import get_connection
from contest_platform.evaluator import evaluate_submission

app = Flask(__name__)

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

def get_app():
    return app

if __name__ == "__main__":
    app.run(debug=True)