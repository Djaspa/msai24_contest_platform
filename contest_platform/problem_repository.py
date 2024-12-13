import json

def load_test_cases(problem_id):
    # Load test cases from a JSON file for simplicity
    with open("tests/test_cases.json", "r") as file:
        test_cases = json.load(file)
    return test_cases.get(str(problem_id), [])

def save_submission_results(submission_id, results):
    with open(f"results_{submission_id}.json", "w") as file:
        json.dump(results, file)