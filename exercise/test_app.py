# test_app.py
import pytest
import subprocess
import time
import functools
import sqlite3
from app import get_raghu_earnings, array_manipulation, decode_matrix

# Decorator to measure execution time and record test result
def timed_test(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        start_time = time.time()
        try:
            result = f(*args, **kwargs)
            duration = time.time() - start_time
            record_test_result('passed', f.__name__, duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            record_test_result('failed', f.__name__, duration, str(e))
            raise
    return wrap

# Function to record the test result in the database
def record_test_result(outcome, test_name, duration, error_message=None):
    timestamp = time.time()
    conn = sqlite3.connect('/workspaces/experiment_python/results/test_results.db')
    with conn:
        conn.execute('''
            INSERT INTO test_results (test_name, outcome, duration, error_message, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (test_name, outcome, duration, error_message, timestamp))
    conn.close()

# Static analysis execution
def run_static_analysis():
    timestamp = time.time()
    try:
        # Analysis with flake8
        result = subprocess.run(['flake8', '--config=/workspaces/experiment_python/.flake8', '/workspaces/experiment_python/exercise/app.py'], capture_output=True, text=True)
        flake8_issues = len(result.stdout.strip().split('\n')) if result.stdout else 0

        # Analysis with mypy
        result = subprocess.run(['mypy', '--config-file=/workspaces/experiment_python/mypy.ini', '/workspaces/experiment_python/exercise/app.py'], capture_output=True, text=True)
        mypy_issues = len(result.stdout.strip().split('\n')) if result.stdout else 0

        # Record results in the database
        conn = sqlite3.connect('/workspaces/experiment_python/results/test_results.db')
        with conn:
            conn.execute('''
                INSERT INTO static_analysis_results (tool, issues, timestamp)
                VALUES (?, ?, ?)
            ''', ('flake8', flake8_issues, timestamp))
            conn.execute('''
                INSERT INTO static_analysis_results (tool, issues, timestamp)
                VALUES (?, ?, ?)
            ''', ('mypy', mypy_issues, timestamp))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

@pytest.fixture(scope="session", autouse=True)
def run_before_tests():
    """
    Run the static analysis before any tests.
    """
    run_static_analysis()

@pytest.mark.parametrize("items_list, orders, expected_output", [
    (["2", "3", "4", "5", "6", "8", "7", "6", "5", "18"], [("6", "55"), ("6", "45"), ("6", "55"), ("4", "40"), ("18", "60"), ("10", "50")], 200),
    (["2", "3", "4", "5", "6"], [("4", "40"), ("3", "30"), ("2", "20")], 90),
    (["5", "5", "5", "5"], [("5", "10"), ("5", "10"), ("5", "10"), ("5", "10"), ("5", "10")], 40),
    (["6", "6", "6"], [("6", "15"), ("6", "20"), ("6", "25"), ("6", "30")], 60),
    (["4", "4", "4", "4", "4", "4"], [("3", "10"), ("3", "10"), ("4", "15"), ("4", "15"), ("4", "15"), ("4", "15")], 60),
])
@timed_test
def test_get_raghu_earnings(items_list, orders, expected_output):
    assert get_raghu_earnings(items_list, orders) == expected_output

@pytest.mark.parametrize(
    "n, queries, expected", [
        (10, [[1, 5, 3], [4, 8, 7], [6, 9, 1]], 10),
        (5, [[1, 2, 100], [2, 5, 100], [3, 4, 100]], 200),
        (10, [[1, 2, 10], [2, 3, 20], [2, 5, 25]], 55),
        (10, [[2, 4, 10], [3, 5, 10], [4, 5, 10]], 30),
        (20, [[1, 3, 2], [2, 5, 3], [4, 8, 7], [5, 9, 6]], 16)
    ]
)
@timed_test
def test_array_manipulation(n, queries, expected):
    assert array_manipulation(n, queries) == expected

@pytest.mark.parametrize("matrix, expected", [
    ([
        ['T', 'h', 'i', 's'],
        ['h', 'i', ' ', 's'],
        ['i', ' ', 'M', 'a'],
        ['s', '%', 'a', 't'],
        ['$', 'M', 't', 'r'],
        ['%', 'a', 'r', 'i'],
        ['x', ' ', 'i', 'x'],
        ['#', ' ', '#', ' '],
        [' ', '%', ' ', '%'],
        ['!', '!', '!', '!']
    ], "This x hi Ma i Matri ssatrix %!"),
    ([
        ['C', 'o', 'd'],
        ['o', 'd', 'i'],
        ['d', 'i', 'n'],
        ['i', 'n', 'g'],
        ['n', 'g', ' '],
        ['g', ' ', 'i'],
        [' ', 'i', 's'],
        ['i', 's', ' '],
        ['s', ' ', 'f'],
        [' ', 'f', 'u'],
        ['f', 'u', 'n'],
        ['u', 'n', '!'],
        ['n', '!', ' ']
    ], "Coding is funoding is fun ding is fun!"),
    ([
        ['H', 'a', 'c'],
        ['a', 'c', 'k'],
        ['c', 'k', 't'],
        ['k', 't', 'o'],
        ['t', 'o', 'b'],
        ['o', 'b', 'e'],
        ['b', 'e', 'r'],
        ['e', 'r', '!']
    ], "Hacktobeacktobercktober!"),
    ([
        ['L', 'e', 't'],
        ['e', 't', '\''],
        ['t', '\'', 's'],
        ['\'', 's', ' '],
        ['s', ' ', 'c'],
        [' ', 'c', 'o'],
        ['c', 'o', 'd'],
        ['o', 'd', 'e'],
        ['d', 'e', '!']
    ], "Let's codet's codet's code!"),
    ([
        ['A', 'l', 'p'],
        ['l', 'p', 'h'],
        ['p', 'h', 'a'],
        ['h', 'a', ' '],
        ['a', ' ', 'n'],
        [' ', 'n', 'u'],
        ['n', 'u', 'm'],
        ['u', 'm', 's'],
        ['m', 's', '!']
    ], "Alpha numlpha numspha nums!")
])
@timed_test
def test_decode_matrix(matrix, expected):
    assert decode_matrix(matrix) == expected

if __name__ == "__main__":
    run_static_analysis()
    pytest.main(['-v'])
