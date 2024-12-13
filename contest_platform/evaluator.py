import subprocess
import json
import os
from sandbox import execute_code
from problem_repository import load_test_cases, save_submission_results

def evaluate_submission(submission):
    try:
        submission_id = submission["submission_id"]
        code = submission["code"]

        with open("submission.py", "w") as file:
            file.write(code)

        test_cases = load_test_cases(submission["problem_id"])

        results = []
        for test_case in test_cases:
            result = execute_code(
                code_file="submission.py",
                input_data=test_case["input_data"],
                expected_output=test_case["expected_output"],
                time_limit=2 
            )
            results.append(result)

            if result["verdict"] != "Passed":
                break  

        save_submission_results(submission_id, results)

        verdict = "Accepted" if all(r["verdict"] == "Passed" for r in results) else results[-1]["verdict"]
        return {"verdict": verdict, "details": results}

    except Exception as e:
        return {"verdict": "System Error", "details": str(e)}