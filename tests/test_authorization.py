import os
import requests

# Read API address and port from environment (for Docker Compose later)
API_ADDRESS = os.environ.get("API_ADDRESS", "localhost")
API_PORT = int(os.environ.get("API_PORT", "8000"))

LOG_ENABLED = os.environ.get("LOG", "0") == "1"
LOG_FILE = "logs/api_test.log"


def run_authz_test(username, password, endpoint, sentence, expected_status):
    """
    Run one authorization test against /v1/sentiment or /v2/sentiment.
    Returns (status_code, test_status, output_text).
    """
    url = f"http://{API_ADDRESS}:{API_PORT}{endpoint}"

    response = requests.get(
        url=url,
        params={
            "username": username,
            "password": password,
            "sentence": sentence,
        },
        timeout=5,
    )

    status_code = response.status_code
    test_status = "SUCCESS" if status_code == expected_status else "FAILURE"

    output = f"""
============================
Authorization test
============================
request done at "{endpoint}"
| username="{username}"
| password="{password}"
| sentence="{sentence}"
expected result = {expected_status}
actual result = {status_code}
==> {test_status}
"""

    return status_code, test_status, output


def log_output(text):
    if LOG_ENABLED:
        with open(LOG_FILE, "a") as f:
            f.write(text)


def main():
    print("### Starting authorization tests ###")

    # Simple sentence; content doesn't matter for authorization
    sentence = "test sentence"

    tests = [
        # bob: only v1 should be allowed
        ("bob", "builder", "/v1/sentiment", sentence, 200),
        ("bob", "builder", "/v2/sentiment", sentence, 403),
        # alice: v1 and v2 should be allowed
        ("alice", "wonderland", "/v1/sentiment", sentence, 200),
        ("alice", "wonderland", "/v2/sentiment", sentence, 200),
    ]

    for username, password, endpoint, sent, expected_status in tests:
        _, _, output = run_authz_test(username, password, endpoint, sent, expected_status)
        print(output)
        log_output(output)

    print("### Authorization tests finished ###")


if __name__ == "__main__":
    main()
