#!/bin/bash

echo "Starting authentication service"
echo "Environment: $env"

# Set the port based on the environment
case "$env" in
  "prod")
    PORT=9000
    ;;
  "uat")
    PORT=9002
    ;;
  "dev")
    PORT=9001
    ;;
  *)
    echo "Unknown environment: $env"
    exit 1
    ;;
esac

# Run Alembic migrations
alembic upgrade head
echo "Port is: $env"

# Start the application with the appropriate port
uvicorn main:app --host 0.0.0.0 --port $PORT
