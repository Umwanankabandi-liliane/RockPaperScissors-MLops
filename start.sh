#!/bin/bash
# Startup script - ensures fresh model download

echo "🔄 Starting FastAPI with model check..."

# Clean up any existing models and zips
echo "🗑️  Cleaning up old models..."
rm -rf models/rps_model
rm -f models/*.zip
rm -f models/model.zip

# Download fresh model
echo "📥 Downloading model from Google Drive..."
python download_model.py

# Verify model exists
if [ -d "models/rps_model" ]; then
    echo "✅ Model ready!"
    ls -la models/rps_model/
else
    echo "❌ Model download failed! Listing models directory:"
    ls -la models/
fi

# Start FastAPI
echo "🚀 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
