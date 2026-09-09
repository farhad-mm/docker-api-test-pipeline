# Sentiment API CI Tests

Author: Farhad Wais

This project defines a simple CI-style test pipeline for the `datascientest/fastapi:1.0.0` sentiment analysis API. The pipeline runs three groups of tests (authentication, authorization, and content) in separate Docker containers, all orchestrated by Docker Compose.

## Structure

- `tests/test_authentication.py`
  Checks that `/permissions` returns the correct status codes for valid and invalid credentials.

- `tests/test_authorization.py`
  Verifies that users have the correct rights on `/v1/sentiment` and `/v2/sentiment` (bob only v1, alice v1 and v2).

- `tests/test_content.py`
  Uses the alice account to ensure both model versions return positive scores for “life is beautiful” and negative scores for “that sucks”.

- `Dockerfile.test`
  Builds the common test image (`tests-image`) from `python:3.11-slim`, installs `requests`, and copies the `tests/` directory.

- `docker-compose.yml`
  Starts the API container and three test containers. Each test container uses the `tests-image`, calls the API via the `api` service name, and writes test results.

- `logs/api_test.log`
  Combined log file with the outputs of all three test groups (generated at runtime, not committed).

- `setup.sh`
  Convenience script that builds `tests-image` and runs `docker compose up` with the test stack.

## How to run

From the project root:

```bash
./setup.sh
```

This will:

1. Build the `tests-image` from `Dockerfile.test`.
2. Start the API and all three test containers via Docker Compose.
3. Stop the stack when tests finish.

The full test report is written to:

```bash
logs/api_test.log
```

The test containers communicate with the API using the service name `api` on port `8000`, and they all share the same `logs/` volume so they append to the same `api_test.log` file.
