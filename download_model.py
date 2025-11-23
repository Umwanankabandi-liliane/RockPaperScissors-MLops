"""
Download model from external source if not present locally.
Use this for deployment when model is too large for Git.
"""
import os
import gdown
import zipfile

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "rps_model")

# Google Drive file ID from your uploaded model
GOOGLE_DRIVE_FILE_ID = "1O6A0JYikCRlW1OF7p7TIAxDtEKTPZ2Zc"
DOWNLOAD_URL = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"

def download_model():
    """Download and extract model if not present."""
    if os.path.exists(MODEL_PATH):
        print(f"✓ Model already exists at {MODEL_PATH}")
        return True
    
    print("📥 Downloading model from Google Drive...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    try:
        # Download zip file with fuzzy matching for large files
        zip_path = os.path.join(MODEL_DIR, "rps_model.zip")
        print(f"Downloading to: {zip_path}")
        print(f"From URL: {DOWNLOAD_URL}")
        
        # Try download with gdown
        output = gdown.download(DOWNLOAD_URL, zip_path, quiet=False, fuzzy=True)
        print(f"Download output: {output}")
        
        # Check if download was successful
        if not os.path.exists(zip_path):
            print(f"❌ Download failed - file not found at {zip_path}")
            print("Trying alternative download method...")
            # Alternative: direct download
            gdown.download(f"https://drive.google.com/uc?export=download&id={GOOGLE_DRIVE_FILE_ID}", 
                          zip_path, quiet=False)
        
        if not os.path.exists(zip_path):
            print("❌ All download methods failed")
            return False
            
        print(f"✅ Downloaded to {zip_path} ({os.path.getsize(zip_path)} bytes)")
        
        # Extract
        print("📦 Extracting model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MODEL_DIR)
        
        # Verify extraction
        if os.path.exists(MODEL_PATH):
            print(f"✅ Model extracted successfully to {MODEL_PATH}")
        else:
            print(f"⚠️  Warning: Expected path {MODEL_PATH} not found after extraction")
        
        # Clean up zip
        os.remove(zip_path)
        print(f"✅ Model ready at {MODEL_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("💡 Please ensure the Google Drive file is shared publicly (Anyone with link can view)")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    download_model()
