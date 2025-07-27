import subprocess
import time
import psutil
import os
import sys
import threading

DEFAULT_TIME_LIMIT = 1.0 
DEFAULT_MEMORY_LIMIT = 256

def get_verdict(user_code_file, input_path, expected_output_path, time_limit, memory_limit_mb):
    if not os.path.exists(user_code_file):
        return "Compilation Error", 0, 0 

    with open(input_path, 'r') as f:
        input_data = f.read()
    with open(expected_output_path, 'r') as f:
        expected_output = f.read().strip()

    start_time = time.time()
    max_memory_usage = 0
    
    process = subprocess.Popen(
        ['python', user_code_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)
    )

    max_memory_usage = 0
    mle_occurred = threading.Event()

    def monitor_memory():
        nonlocal max_memory_usage
        ps_process = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                current_memory = ps_process.memory_info().rss / (1024 * 1024)
                if current_memory > max_memory_usage:
                    max_memory_usage = current_memory
                
                if max_memory_usage > memory_limit_mb:
                    mle_occurred.set() 
                    psutil.Process(process.pid).kill()
                    break
                time.sleep(0.05) 
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
    
    monitor_thread = threading.Thread(target=monitor_memory)
    monitor_thread.start()
    
    start_time = time.time()

    try:
        stdout, stderr = process.communicate(input=input_data, timeout=time_limit)
        execution_time = time.time() - start_time
        
        monitor_thread.join()

        if mle_occurred.is_set():
            return "Memory Limit Exceeded", execution_time, max_memory_usage

        if process.returncode != 0:
            return "Runtime Error", execution_time, max_memory_usage

        user_output = stdout.strip()

        if user_output == expected_output:
            return "Accepted", execution_time, max_memory_usage
        else:
            return "Wrong Answer", execution_time, max_memory_usage

    except subprocess.TimeoutExpired:
        process.kill()
        execution_time = time.time() - start_time
        monitor_thread.join()
        return "Time Limit Exceeded", execution_time, max_memory_usage
    except Exception as e:
        process.kill()
        monitor_thread.join()
        return f"Judge Error: {e}", 0, 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python judge.py <solution_file> <input_file> <expected_output_file>")
        sys.exit(1)

    user_code_file = sys.argv[1]
    input_file = sys.argv[2]
    expected_output_file = sys.argv[3]
    
    verdict, exec_time, mem_usage = get_verdict(
        user_code_file,
        input_file,
        expected_output_file,
        DEFAULT_TIME_LIMIT,
        DEFAULT_MEMORY_LIMIT
    )
    
    print(f"Verdict: {verdict}")
    print(f"Execution Time: {exec_time:.4f} s")
    print(f"Memory Usage: {mem_usage:.2f} MB")