#!/bin/bash
# Startup script - ensures fresh model download

echo "🔄 Starting FastAPI with model check..."

# Remove old model if it exists
if [ -d "models/rps_model" ]; then
    echo "🗑️  Removing old model..."
    rm -rf models/rps_model
fi

# Download model
echo "📥 Downloading model..."
python download_model.py

# Start FastAPI
echo "🚀 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
