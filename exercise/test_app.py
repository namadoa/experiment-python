# test_app.py
import pytest
import subprocess
import time
import sqlite3
from app import add

# Decorator to measure execution time and record test result
def timed_test(f):
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

# Pytest fixture to run before tests
@pytest.fixture(scope="session", autouse=True)
def run_before_tests():
    """
    Run the static analysis before any tests.
    """
    run_static_analysis()

# Test functions
@timed_test
def test_add():
    assert add(1, 2) == 3
    assert add(5, 7) == 12

if __name__ == "__main__":
    # Ejecutar análisis estático y guardar resultados
    run_static_analysis()
    
    # Ejecutar todas las pruebas con pytest
    pytest.main(['-v'])
