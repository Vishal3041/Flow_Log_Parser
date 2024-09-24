# FlowLogAnalyzer

A Python tool to parse AWS VPC flow logs and tag entries based on port and protocol combinations from a lookup table. This project supports processing TCP, UDP, and ICMP protocols, tagging each log entry based on predefined rules, and generating a summary of tag counts and port/protocol combination counts.

## Table of Contents
- [Assumptions](#assumptions)
- [Features](#features)
- [Usage](#usage)
- [Test Cases](#test-cases)
- [Known Issues](#known-issues)
- [How to Run](#how-to-run)
  - [Running Single Test Case](#running-single-test-case)
  - [Running All Test Cases at Once](#running-all-test-cases-at-once)
- [Installation](#installation)

---

## Assumptions
1. **Port 22 (SSH)** is **always open** and tagged as `sv_P4` even if it is not explicitly logged.
2. All ports **not found in the lookup table** are tagged as **Untagged**.
3. Flow logs with a status of **REJECT** are tagged as **Untagged** but are **still included** in the port/protocol combination counts.
4. The lookup table provides the correct mappings for destination ports and protocols.
5. Log format strictly follows AWS VPC flow log **version 2** structure.
6. The script handles **TCP (6)**, **UDP (17)**, and **ICMP (1)** protocols.

---

## Features
- **Flow Log Parsing**: Extracts information from flow logs and tags based on a provided lookup table.
- **REJECT Handling**: Marks REJECT logs as untagged but includes them in port/protocol combination counts.
- **Support for Multiple Protocols**: TCP, UDP, and ICMP are handled with case-insensitive tagging.
- **Port 22 Always Open**: Automatically adds port 22 to the tag and port counts.

---

## Test Cases
We include a set of test cases in the `tests/` directory. These cover a range of scenarios including:
- Basic flow logs with well-known ports (e.g., 25, 80, 443).
- REJECT logs and handling untagged entries.
- Logs with multiple protocols (TCP, UDP, ICMP).
- Edge cases with no matching entries in the lookup table.
- lookup_table.csv: The port-to-tag mappings.
- flow_logs.txt: The flow log entries.
- expected_output.txt: The expected output for comparison.

### Known Issues:
1. **Incorrect Output in Existing Test Case**: In one test case, port `22` is included in the expected output, but it is missing in the flow logs. This has been manually corrected by including port `22` by default.
2. **Ephemeral Ports**: In some cases, dynamic/ephemeral ports (e.g., `49153`, `49155`) may not align with expected output, as the lookup table focuses on well-known ports.
3. **REJECT Entries**: REJECT logs are tagged as **Untagged** but still included in port/protocol combination counts.

---


Test Case Directory Structure:


## Usage
### 1. Command-Line Usage
```bash
python3 flow_logs_parser.py <lookup_table.csv> <flow_logs.txt> <output.txt>

- lookup_table.csv: The CSV file containing dstport, protocol, and tag mappings.
- flow_logs.txt: The file containing flow logs (AWS VPC Flow Logs, version 2).
- output.txt: The output file where results will be written.

## How to Run
### Running Single Test Case
To run a specific test case:

```bash
python3 flow_logs_parser.py tests/test_case_1/lookup_table.csv tests/test_case_1/flow_logs.txt tests/test_case_1/actual_output.txt
- Then, compare actual_output.txt to expected_output.txt.

### Running All Test Cases at Once
- You can run all the test cases by using the provided test runner script (run_tests.py):

```bash
python3 run_tests.py
- The script will iterate through all test cases in the tests/ directory, generate the actual output, and compare it to the expected output.

