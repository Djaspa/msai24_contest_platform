from contest_platform.sandbox import execute_code
from contest_platform.problem_repository import load_test_cases, save_submission_results, save_submission, fetch_next_submission, update_submission_status
import threading
import time
import uuid

class WorkerManager:
    def __init__(self, num_workers=2, heartbeat_interval=2, timeout=10):
        self.num_workers = num_workers
        self.heartbeat_interval = heartbeat_interval
        self.timeout = timeout
        self.workers = {}
        self.worker_threads = {}
        self.lock = threading.Lock()
        self.restart_events = {}

    def start(self):
        for i in range(self.num_workers):
            worker_id = str(uuid.uuid4())
            self._start_worker(worker_id)

    def _start_worker(self, worker_id):
        restart_event = threading.Event()
        t = threading.Thread(target=self.worker_loop, args=(worker_id, restart_event), daemon=True)
        with self.lock:
            self.workers[worker_id] = {
                'last_heartbeat': time.time(),
                'current_load': 0,
                'is_live': True,
                'thread': t,
                'restart_event': restart_event
            }
            self.worker_threads[worker_id] = t
            self.restart_events[worker_id] = restart_event
        t.start()

    def worker_loop(self, worker_id, restart_event):
        while True:
            with self.lock:
                self.workers[worker_id]['last_heartbeat'] = time.time()
                self.workers[worker_id]['is_live'] = True
            submission = fetch_next_submission()
            if submission:
                with self.lock:
                    self.workers[worker_id]['current_load'] = 1
                try:
                    update_submission_status(submission['submission_id'], 'Processing')
                    code = submission["code"]
                    language = submission.get("language", "python")
                    if language == "java":
                        code_file = "Main.java"
                    else:
                        code_file = "submission.py"
                    with open(code_file, "w") as file:
                        file.write(code)
                    test_cases = load_test_cases(submission["problem_id"])
                    results = []
                    for test_case in test_cases:
                        result = execute_code(
                            code_file=code_file,
                            input_data=test_case["input_data"],
                            expected_output=test_case["expected_output"],
                            time_limit=2,
                            language=language
                        )
                        results.append(result)
                        if result["verdict"] != "Passed":
                            break
                    save_submission_results(submission['submission_id'], results)
                    verdict = "Accepted" if all(r["verdict"] == "Passed" for r in results) else results[-1]["verdict"]
                    update_submission_status(submission['submission_id'], 'Finished', verdict)
                except Exception as e:
                    update_submission_status(submission['submission_id'], 'Error', str(e))
                finally:
                    with self.lock:
                        self.workers[worker_id]['current_load'] = 0
            else:
                with self.lock:
                    self.workers[worker_id]['current_load'] = 0
                if restart_event.wait(timeout=self.heartbeat_interval):
                    restart_event.clear()
                    break
            
            with self.lock:
                self.workers[worker_id]['last_heartbeat'] = time.time()
            time.sleep(self.heartbeat_interval)

    def get_status(self):
        with self.lock:
            now = time.time()
            status = {}
            for worker_id, info in self.workers.items():
                is_live = (now - info['last_heartbeat']) < self.timeout and info['thread'].is_alive()
                status[worker_id] = {
                    'is_live': is_live,
                    'current_load': info['current_load'],
                    'last_heartbeat': info['last_heartbeat']
                }
                self.workers[worker_id]['is_live'] = is_live
            return status

    def restart_dead_workers(self):
        with self.lock:
            for worker_id, info in list(self.workers.items()):
                if not info['is_live'] or not info['thread'].is_alive():
                    print(f"Restarting worker {worker_id}")
                    self.restart_events[worker_id].set()
                    
                    del self.workers[worker_id]
                    del self.worker_threads[worker_id]
                    del self.restart_events[worker_id]
                    
                    new_worker_id = str(uuid.uuid4())
                    self._start_worker(new_worker_id)

worker_manager = None

def start_workers(num_workers=2):
    global worker_manager
    worker_manager = WorkerManager(num_workers=num_workers)
    worker_manager.start()
    # Start a monitor thread to restart dead workers
    def monitor():
        while True:
            worker_manager.restart_dead_workers()
            time.sleep(5)
    threading.Thread(target=monitor, daemon=True).start()
    return worker_manager

def get_worker_status():
    global worker_manager
    if worker_manager:
        return worker_manager.get_status()
    return {}