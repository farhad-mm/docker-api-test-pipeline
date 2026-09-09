#!/usr/bin/env bash
set -e

echo "Building tests image..."
docker build -f Dockerfile.test -t tests-image .

echo "Starting API and tests with docker compose..."
docker compose up --abort-on-container-exit --remove-orphans

echo "All containers have finished."
echo "Combined test log is in ./logs/api_test.log"
