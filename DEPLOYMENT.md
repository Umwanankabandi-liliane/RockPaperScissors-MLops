# How to Deploy with Large Model Files

## Option 1: Git LFS (Recommended)

Already configured! Once your internet connection is stable:

```bash
git push origin main
```

Git LFS will handle the large files automatically.

## Option 2: Download Model at Deployment

### Steps:

1. **Upload your model to Google Drive:**
   - Zip the `models/` folder
   - Upload to Google Drive
   - Right-click → Get shareable link
   - Extract the FILE_ID from the link
   - Update `GOOGLE_DRIVE_FILE_ID` in `download_model.py`

2. **Add to requirements.txt:**
   ```
   gdown
   ```

3. **Modify your app startup:**
   Add this to the top of `main.py`:
   ```python
   from download_model import download_model
   download_model()
   ```

4. **Update .gitignore:**
   ```
   models/
   ```

5. **Push to GitHub** (without models)

6. **Deploy** - Model downloads automatically on first run

## Option 3: HuggingFace Hub

```python
# Upload model
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path="models/rps_model",
    repo_id="your-username/rps-model",
    repo_type="model"
)

# Download in deployment
from huggingface_hub import hf_hub_download
model_path = hf_hub_download(
    repo_id="your-username/rps-model",
    filename="saved_model.pb"
)
```

## Current Status:
✅ Git LFS configured
✅ `.gitattributes` created
✅ `.gitignore` created
⏳ Pending: Push to GitHub (network issue)
