from contest_platform.evaluator import evaluate_submission
from api.api import get_app

def main():
    submission = {
        "submission_id": None,
        "user_id": 101,
        "problem_id": 202,
        "code": f'def solve():\n\tprint(input())\nsolve()',
        "language": "python",
    }

    result = evaluate_submission(submission)
    print("Final Verdict:", result["verdict"])
    print("Details:", result)

if __name__ == "__main__":
    #main()
    app = get_app()
    app.run()