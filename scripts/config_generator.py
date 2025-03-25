import json
import os

CONFIG_FILE = "tester_config.json"
VALID_FILE = "valid_files"

def generate_config(solution_file, project_type, test_num = 5):
    config = {
        "version": 2,
        "python_version": 3.9,
        "solution_signature": f"solution/{solution_file}",
        "number_of_tests": test_num,
        "can_submit_single_file": True,
        "single_file_path": f"solution/{solution_file}",
        "packages": [
            {
                "name": project_type,
                "score": 100,
                "tests": [f"test_{i+1}" for i in range(test_num)],
                "aggregator": "sum"
            }
        ]
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print(f"✅ Configuration file '{CONFIG_FILE}' generated successfully.")

def generate_valid_files(solution_file):
    with open(VALID_FILE, "w") as f:
        f.write(f"solution/{solution_file}")

    print(f"✅ Valid files '{VALID_FILE}' generated successfully.")
