# msai24_contest_platform
Current Features

* Create and list programming problems

* Add test cases to problems

* Submit code for evaluation

* List user submissions with filters

# Setup

Install dependencies and run server:

`pip install -r requirements.txt`

`python3 setup_db.py`

`python3 main.py`

The API server will start at http://127.0.0.1:5000

# Simple requests

Create problem
```
curl -X POST http://127.0.0.1:5000/problem/create_problem \
-H "Content-Type: application/json" \
-d '{
    "title": "Sum of Two Numbers",
    "description": "Write a program to add two numbers.",
    "time_limit": 2.0,
    "memory_limit": 256
}'
```

Add test case to a problem
```
curl -X POST http://127.0.0.1:5000/problem/add_test_case \
-H "Content-Type: application/json" \
-d '{
    "problem_id": 1,
    "input_data": "3 5",
    "expected_output": "8"
}'
```

List problems

`curl -X GET http://127.0.0.1:5000/problem/list`

Submit solution 

```
curl -X POST http://127.0.0.1:5000/user/submit \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "problem_id": 1,
    "code": "print(sum(map(int, input().split())))",
    "language": "python"
}'
```

List submissions
```
curl -X GET "http://127.0.0.1:5000/user/submissions_list?user_id=1&problem_id=1"
```