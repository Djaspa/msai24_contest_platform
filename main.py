from contest_platform.evaluator import evaluate_submission, start_workers
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
    start_workers(num_workers=2)
    app = get_app()
    app.run(host='0.0.0.0', port=5000)