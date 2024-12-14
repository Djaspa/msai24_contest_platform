import sqlite3
from db_config import DATABASE_PATH

def initialize_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Problems (
        problem_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        time_limit REAL NOT NULL,
        memory_limit INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestCases (
        test_case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER NOT NULL,
        input_data TEXT NOT NULL,
        expected_output TEXT NOT NULL,
        FOREIGN KEY (problem_id) REFERENCES Problems(problem_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Submissions (
        submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        problem_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        language TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        verdict TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (problem_id) REFERENCES Problems(problem_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SubmissionResults (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER NOT NULL,
        test_case_id INTEGER NOT NULL,
        execution_time REAL,
        memory_used INTEGER,
        verdict TEXT,
        FOREIGN KEY (submission_id) REFERENCES Submissions(submission_id),
        FOREIGN KEY (test_case_id) REFERENCES TestCases(test_case_id)
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")