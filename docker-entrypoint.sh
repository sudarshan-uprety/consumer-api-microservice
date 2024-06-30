#!/bin/bash

echo "Starting authentication service"
echo "Environment: $env"

# Set the port based on the environment
case "$env" in
  "prod")
    PORT=9002
    ;;
  "uat")
    PORT=9001
    ;;
  "dev")
    PORT=9000
    ;;
  *)
    echo "Unknown environment: $env"
    exit 1
    ;;
esac

# Run Alembic migrations
alembic upgrade head

# Start the application with the appropriate port
uvicorn main:app --host 0.0.0.0 --port $PORT
