import sqlite3
from config import DATABASE_PATH

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def load_test_cases(problem_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT input_data, expected_output FROM TestCases WHERE problem_id = ?", (problem_id,))
    test_cases = cursor.fetchall()
    connection.close()
    return [{"input_data": tc[0], "expected_output": tc[1]} for tc in test_cases]

def save_submission(submission):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO Submissions (user_id, problem_id, code, language, verdict)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        submission["user_id"],
        submission["problem_id"],
        submission["code"],
        submission["language"],
        submission.get("verdict", None)
    ))
    submission_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return submission_id

def save_submission_results(submission_id, results):
    connection = get_connection()
    cursor = connection.cursor()

    for result in results:
        cursor.execute('''
        INSERT INTO SubmissionResults (submission_id, test_case_id, execution_time, memory_used, verdict)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            submission_id,
            result.get("test_case_id"),
            result.get("execution_time"),
            result.get("memory_used"),
            result.get("verdict")
        ))

    connection.commit()
    connection.close()