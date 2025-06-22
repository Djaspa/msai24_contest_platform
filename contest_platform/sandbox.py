import subprocess
import os

def execute_code(code_file, input_data, expected_output, time_limit, language='python'):
    try:
        if language == 'python':
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
        elif language == 'java':
            compile_proc = subprocess.run(
                ["javac", code_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if compile_proc.returncode != 0:
                return {"verdict": "Compile Error", "details": compile_proc.stderr.decode()}
            run_proc = subprocess.run(
                ["java", "Main"],
                input=input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=time_limit,
                cwd=os.path.dirname(code_file) or None
            )
            if run_proc.returncode != 0:
                return {"verdict": "Runtime Error", "details": run_proc.stderr.decode()}
            output = run_proc.stdout.decode().strip()
        else:
            return {"verdict": "System Error", "details": f"Unsupported language: {language}"}

        if output == expected_output:
            return {"verdict": "Passed"}
        else:
            return {"verdict": "Wrong Answer", "output": output}

    except subprocess.TimeoutExpired:
        return {"verdict": "Time Limit Exceeded"}
    except Exception as e:
        return {"verdict": "Runtime Error", "details": str(e)}