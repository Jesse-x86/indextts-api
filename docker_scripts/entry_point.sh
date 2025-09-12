#!/bin/bash
set -e

echo "=== Running entry_point.sh ==="

# Define the directories and ports based on the environment variables
# This will use the values from the Dockerfile unless overridden
MODEL_CHECKPOINT_DIR=${MODEL_CHECKPOINT_DIR}
MODEL_V2_CHECKPOINT_DIR=${MODEL_V2_CHECKPOINT_DIR}
REFERENCE_VOICE_DIR=${REFERENCE_VOICE_DIR}
PROJECT_ROOT=${PROJECT_ROOT}
HOST=${API_HOST:-"0.0.0.0"}
PORT=${API_PORT:-"8198"}

# Step 1: Check and download required models
echo "⚙️  Ensuring models and reference audio are available..."
"${PROJECT_ROOT}/docker_scripts/ensure_models.sh" "$MODEL_CHECKPOINT_DIR" "$REFERENCE_VOICE_DIR"
"${PROJECT_ROOT}/docker_scripts/ensure_models_v2.sh" "$MODEL_V2_CHECKPOINT_DIR"

echo "✅ Models are ready."

# Step 2: Start the application with Uvicorn
echo "🚀 Starting Uvicorn server..."
uvicorn api.main:app --host "$HOST" --port "$PORT" --log-config "${PROJECT_ROOT}/uvicorn_logging_config.ini"
echo "❌ Uvicorn server exited."