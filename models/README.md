# Models Directory

This folder should contain the trained model files.

## Expected Structure:
```
models/
└── rps_model/
    ├── saved_model.pb
    ├── fingerprint.pb
    └── variables/
        ├── variables.data-00000-of-00001
        └── variables.index
```

## How to get the model:

### Option 1: Download from Google Drive
[Add your Google Drive link here]

### Option 2: Train the model
```bash
python train_model.py
```

This will train a new model and save it to this directory.

### Option 3: Download during deployment
The `download_model.py` script can automatically download the model.
