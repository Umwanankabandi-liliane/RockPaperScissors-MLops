"""
Download model from external source if not present locally.
Use this for deployment when model is too large for Git.
"""
import os
import gdown
import zipfile

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "rps_model")

# Replace with your Google Drive file ID or direct link
GOOGLE_DRIVE_FILE_ID = "YOUR_FILE_ID_HERE"  # Get from shareable link
DOWNLOAD_URL = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"

def download_model():
    """Download and extract model if not present."""
    if os.path.exists(MODEL_PATH):
        print(f"✓ Model already exists at {MODEL_PATH}")
        return True
    
    print("📥 Downloading model from Google Drive...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    try:
        # Download zip file
        zip_path = os.path.join(MODEL_DIR, "model.zip")
        gdown.download(DOWNLOAD_URL, zip_path, quiet=False)
        
        # Extract
        print("📦 Extracting model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MODEL_DIR)
        
        # Clean up zip
        os.remove(zip_path)
        print(f"✅ Model downloaded and extracted to {MODEL_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

if __name__ == "__main__":
    download_model()
