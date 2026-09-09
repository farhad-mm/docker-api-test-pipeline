import os
import requests

API_ADDRESS = os.environ.get("API_ADDRESS", "localhost")
API_PORT = int(os.environ.get("API_PORT", "8000"))

LOG_ENABLED = os.environ.get("LOG", "0") == "1"
LOG_FILE = "logs/api_test.log"


def run_content_test(version, sentence, expected_sign):
    """
    version: "v1" or "v2"
    sentence: text to analyze
    expected_sign: "positive" or "negative"
    """
    endpoint = f"/{version}/sentiment"
    url = f"http://{API_ADDRESS}:{API_PORT}{endpoint}"

    response = requests.get(
        url=url,
        params={
            "username": "alice",
            "password": "wonderland",
            "sentence": sentence,
        },
        timeout=5,
    )

    status_code = response.status_code
    test_status = "FAILURE"
    score = None
    score_ok = False

    if status_code == 200:
        data = response.json()
        # Adjust key name if /docs shows something different
        score = data.get("sentiment") or data.get("score") or data.get("prediction")
        if score is not None:
            if expected_sign == "positive":
                score_ok = score > 0
            elif expected_sign == "negative":
                score_ok = score < 0

    if status_code == 200 and score_ok:
        test_status = "SUCCESS"

    output = f"""
============================
Content test
============================
request done at "{endpoint}"
| username="alice"
| password="wonderland"
| sentence="{sentence}"
expected sign = {expected_sign}
status code = {status_code}
returned score = {score}
==> {test_status}
"""

    return status_code, score, test_status, output


def log_output(text):
    if LOG_ENABLED:
        with open(LOG_FILE, "a") as f:
            f.write(text)


def main():
    print("### Starting content tests ###")

    tests = [
        ("v1", "life is beautiful", "positive"),
        ("v1", "that sucks", "negative"),
        ("v2", "life is beautiful", "positive"),
        ("v2", "that sucks", "negative"),
    ]

    for version, sentence, expected_sign in tests:
        _, _, _, output = run_content_test(version, sentence, expected_sign)
        print(output)
        log_output(output)

    print("### Content tests finished ###")


if __name__ == "__main__":
    main()
