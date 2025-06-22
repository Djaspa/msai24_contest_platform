# msai24_contest_platform
Current Features

* Create and list programming problems

* Add test cases to problems

* Submit code for evaluation

* List user submissions with filters

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

# Docker

You can run the project using Docker:

1. Build the Docker image:

```
docker build -t msai24_contest_platform .
```

2. Run the container:

```
docker run -p 5000:5000 msai24_contest_platform
```

The app will be available at http://127.0.0.1:5000