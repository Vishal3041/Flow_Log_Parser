import os
import subprocess


def run_test(test_dir):
    # Set paths for the test case
    lookup_table = os.path.join(test_dir, 'lookup_table.csv')
    flow_logs = os.path.join(test_dir, 'flow_logs')
    expected_output = os.path.join(test_dir, 'expected_output')
    actual_output = os.path.join(test_dir, 'output')

    # Run the flow_logs_parser.py script with the test files
    try:
        subprocess.run(['python3', 'flow_logs_parser.py', lookup_table, flow_logs, actual_output], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running test case: {test_dir}")
        print(f"Command failed with error: {e}")
        return

    # Compare actual output to expected output
    with open(expected_output, 'r') as expected_file, open(actual_output, 'r') as actual_file:
        expected_data = expected_file.read().strip()
        actual_data = actual_file.read().strip()

        if expected_data == actual_data:
            print(f"Test passed: {test_dir}")
        else:
            print(f"Test failed: {test_dir}")
            print("Expected Output:")
            print(expected_data)
            print("Actual Output:")
            print(actual_data)


if __name__ == "__main__":
    # Define your test cases directories
    test_cases = ['test_cases/test1', 'test_cases/test2', 'test_cases/test3', 'test_cases/test4',
                    'test_cases/test6', 'test_cases/test7', 'test_cases/test5']

    # Run tests
    for test_case in test_cases:
        run_test(test_case)
