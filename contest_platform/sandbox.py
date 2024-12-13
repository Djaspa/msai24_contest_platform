import subprocess

def execute_code(code_file, input_data, expected_output, time_limit):
    try:
        process = subprocess.run(
            ["python3", code_file],
            input=input_data.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=time_limit
        )

        if process.returncode != 0:
            return {"verdict": "Runtime Error", "details": process.stderr.decode()}

        output = process.stdout.decode().strip()
        if output == expected_output:
            return {"verdict": "Passed"}
        else:
            return {"verdict": "Wrong Answer", "output": output}

    except subprocess.TimeoutExpired:
        return {"verdict": "Time Limit Exceeded"}
    except Exception as e:
        return {"verdict": "Runtime Error", "details": str(e)}