#!/bin/bash

# Docker container name or ID
CONTAINER_NAME="backend-api-1"

# SSH into the Docker container
docker exec -it $CONTAINER_NAME sh

# Once you're inside the container, you can run pytest
# For example:
pytest tests/test_*.py