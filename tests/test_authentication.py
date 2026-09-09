import os
import requests

# Read API address and port from environment (useful for Docker Compose later)
API_ADDRESS = os.environ.get("API_ADDRESS", "localhost")
API_PORT = int(os.environ.get("API_PORT", "8000"))

LOG_ENABLED = os.environ.get("LOG", "0") == "1"
LOG_FILE = "logs/api_test.log"


def run_test(username, password, expected_status):
    """
    Run one authentication test against /permissions.
    Returns a tuple: (status_code, test_status, output_text)
    """
    url = f"http://{API_ADDRESS}:{API_PORT}/permissions"

    response = requests.get(
        url=url,
        params={
            "username": username,
            "password": password,
        },
        timeout=5,
    )

    status_code = response.status_code
    test_status = "SUCCESS" if status_code == expected_status else "FAILURE"

    output = f"""
============================
Authentication test
============================
request done at "/permissions"
| username="{username}"
| password="{password}"
expected result = {expected_status}
actual result = {status_code}
==> {test_status}
"""

    return status_code, test_status, output


def log_output(text):
    """
    Append text to the log file if LOG is enabled.
    """
    if LOG_ENABLED:
        with open(LOG_FILE, "a") as f:
            f.write(text)


def main():
    """
    Run all authentication scenarios.
    """
    print("### Starting authentication tests ###")

    tests = [
        # (username, password, expected_status)
        ("alice", "wonderland", 200),
        ("bob", "builder", 200),
        ("alice", "clementine", 403),
    ]

    for username, password, expected_status in tests:
        _, _, output = run_test(username, password, expected_status)
        print(output)
        log_output(output)

    print("### Authentication tests finished ###")


if __name__ == "__main__":
    main()
