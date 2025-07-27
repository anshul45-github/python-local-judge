# Python Local Judge 🚀

A lightweight, local judge written in Python to test programming solutions. This script simulates a competitive programming environment by enforcing strict **time** and **memory** limits, providing verdicts like those found on Codeforces.

-----

## \#\# Features

  - **Time Limit Enforcement (TLE)**: Automatically terminates solutions that run too long.
  - **Memory Limit Enforcement (MLE)**: Kills processes that exceed the defined memory allocation.
  - **Concurrent Monitoring**: Uses threading to monitor memory usage in real-time while handling I/O and time limits.
  - **Comprehensive Verdicts**: Reports **Accepted (AC)**, **Wrong Answer (WA)**, **Runtime Error (RE)**, **TLE**, and **MLE**.
  - **Command-Line Interface**: Flexible and easy to use by passing file paths as arguments.
  - **Cross-Platform**: Works on Windows, Linux, and macOS.

-----

## \#\# Project Structure

Organize your files as shown below for the judge to work seamlessly.

```
.
├── 🐍 judge.py
├── 📝 requirements.txt
├── 📂 solutions/
│   ├── sum_problem.py
│   ├── tle_problem.py
│   └── mle_problem.py
└── 📂 testcases/
    ├── sum_input.txt
    └── sum_expected.txt
```

-----

## \#\# Setup

1.  **Prerequisites**: Make sure you have **Python 3.9+** installed.

2.  **Clone the Repository**:

    ```bash
    git clone https://github.com/anshul45-github/python-local-judge
    cd python-local-judge
    ```

3.  **Create `requirements.txt`**: Create a file named `requirements.txt` with the following content:

    ```
    psutil
    ```

4.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

-----

## \#\# Usage

Run the judge from your terminal using the following format.

### **Command Format**

```bash
python judge.py <path_to_solution> <path_to_input> <path_to_expected_output>
```

### **Example Test Cases**

#### ✅ Accepted (AC)

  - **Solution**: A correct program that solves the problem.
  - **Command**:
    ```bash
    python judge.py solutions/sum_problem.py testcases/sum_input.txt testcases/sum_expected.txt
    ```

#### ⏳ Time Limit Exceeded (TLE)

  - **Solution**: A program with an infinite loop.
  - **Command**:
    ```bash
    python judge.py solutions/tle_problem.py testcases/sum_input.txt testcases/sum_expected.txt
    ```

#### 🧠 Memory Limit Exceeded (MLE)

  - **Solution**: A program that allocates a very large amount of memory.
  - **Command**:
    ```bash
    python judge.py solutions/mle_problem.py testcases/sum_input.txt testcases/sum_expected.txt
    ```

#### ❌ Wrong Answer (WA)

  - **Solution**: A program that produces incorrect output.
  - **Command**:
    ```bash
    python judge.py solutions/wa_problem.py testcases/sum_input.txt testcases/sum_expected.txt
    ```

#### 💥 Runtime Error (RE)

  - **Solution**: A program that crashes (e.g., division by zero).
  - **Command**:
    ```bash
    python judge.py solutions/re_problem.py testcases/empty_input.txt testcases/empty_expected.txt
    ```

-----

## \#\# How It Works

  - The user's code runs in an isolated child process using **`subprocess.Popen`**.
  - A separate **`threading.Thread`** monitors the process's memory usage in real-time with the **`psutil`** library. If the memory limit is exceeded, the monitor thread kills the process.
  - The main thread calls **`process.communicate()`** with a `timeout`. This sends input data, captures output, and enforces the time limit simultaneously.
  - The final verdict is determined by the process's exit code, results from the monitor thread, and comparing the program's output with the expected output.