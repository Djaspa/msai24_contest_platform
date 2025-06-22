import sqlite3
from config.db_config import DATABASE_PATH

def insert_initial_data():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Problem 1: Add Two Numbers
    cursor.execute('''
        INSERT INTO Problems (title, description, time_limit, memory_limit)
        VALUES (?, ?, ?, ?)
    ''', (
        'Add Two Numbers',
        'Given two integers, output their sum.\nInput: Two integers separated by space.\nOutput: Their sum.',
        2.0, 256
    ))
    problem1_id = cursor.lastrowid
    test_cases1 = [
        (problem1_id, '1 2', '3'),
        (problem1_id, '10 20', '30'),
        (problem1_id, '-5 5', '0'),
        (problem1_id, '100 200', '300'),
        (problem1_id, '0 0', '0'),
        (problem1_id, '-10 -20', '-30'),
        (problem1_id, '123 456', '579'),
        (problem1_id, '999 1', '1000'),
        (problem1_id, '-100 50', '-50'),
        (problem1_id, '2147483647 -1', '2147483646'),
    ]
    cursor.executemany('''
        INSERT INTO TestCases (problem_id, input_data, expected_output)
        VALUES (?, ?, ?)
    ''', test_cases1)

    # Problem 2: Reverse String
    cursor.execute('''
        INSERT INTO Problems (title, description, time_limit, memory_limit)
        VALUES (?, ?, ?, ?)
    ''', (
        'Reverse String',
        'Given a string, output its reverse.\nInput: A string.\nOutput: The reversed string.',
        2.0, 256
    ))
    problem2_id = cursor.lastrowid
    test_cases2 = [
        (problem2_id, 'hello', 'olleh'),
        (problem2_id, 'world', 'dlrow'),
        (problem2_id, 'abc', 'cba'),
        (problem2_id, 'a', 'a'),
        (problem2_id, '', ''),
        (problem2_id, 'racecar', 'racecar'),
        (problem2_id, 'Python', 'nohtyP'),
        (problem2_id, '12345', '54321'),
        (problem2_id, 'OpenAI', 'IAnepO'),
        (problem2_id, 'test case', 'esac tset'),
    ]
    cursor.executemany('''
        INSERT INTO TestCases (problem_id, input_data, expected_output)
        VALUES (?, ?, ?)
    ''', test_cases2)

    # Problem 3: FizzBuzz
    cursor.execute('''
        INSERT INTO Problems (title, description, time_limit, memory_limit)
        VALUES (?, ?, ?, ?)
    ''', (
        'FizzBuzz',
        'Given an integer n, print numbers from 1 to n. For multiples of 3 print "Fizz" instead of the number, for multiples of 5 print "Buzz", and for multiples of both print "FizzBuzz".\nInput: An integer n.\nOutput: The FizzBuzz sequence as a space-separated string.',
        2.0, 256
    ))
    problem3_id = cursor.lastrowid
    test_cases3 = [
        (problem3_id, '5', '1 2 Fizz 4 Buzz'),
        (problem3_id, '1', '1'),
        (problem3_id, '3', '1 2 Fizz'),
        (problem3_id, '10', '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz'),
        (problem3_id, '15', '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz'),
        (problem3_id, '0', ''),
        (problem3_id, '2', '1 2'),
        (problem3_id, '6', '1 2 Fizz 4 Buzz Fizz'),
        (problem3_id, '8', '1 2 Fizz 4 Buzz Fizz 7 8'),
        (problem3_id, '20', '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz'),
    ]
    cursor.executemany('''
        INSERT INTO TestCases (problem_id, input_data, expected_output)
        VALUES (?, ?, ?)
    ''', test_cases3)

    connection.commit()
    connection.close()
    print('Initial problems and test cases inserted.')

if __name__ == "__main__":
    insert_initial_data() 