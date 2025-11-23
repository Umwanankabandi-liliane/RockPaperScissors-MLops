from fastapi import FastAPI, UploadFile, File
import numpy as np
from PIL import Image
import io
import time
import os
import tensorflow as tf

app = FastAPI()

# ===============================
# LOAD MODEL
# ===============================
MODEL_PATH = "models/rps_model"
H5_MODEL_PATH = "models/rps_model.h5"

# Try loading model
model = None
try:
    if os.path.exists(MODEL_PATH):
        print(f"Loading SavedModel from {MODEL_PATH}...")
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ SavedModel loaded successfully")
    elif os.path.exists(H5_MODEL_PATH):
        print(f"Loading H5 model from {H5_MODEL_PATH}...")
        model = tf.keras.models.load_model(H5_MODEL_PATH)
        print("✅ H5 Model loaded successfully")
    else:
        print("⚠️  No model found! Run build.py or train_model.py first.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Class names (MUST match order used during training)
class_names = ["Rock", "Paper", "Scissors"]

# Track server start time
start_time = time.time()


@app.get("/")
def home():
    return {"message": "Rock-Paper-Scissors API is running!"}


@app.get("/uptime")
def uptime():
    return {"uptime_seconds": time.time() - start_time}


# ===============================
# 📌 PREDICT ENDPOINT
# ===============================
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model not loaded. Please check server logs."}
    
    try:
        # Read bytes
        contents = await file.read()

        # Load image
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image = image.resize((150, 150))

        # Preprocess
        img_array = np.array(image).astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Run prediction
        preds = model.predict(img_array, verbose=0)

        idx = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]))

        return {
            "prediction": class_names[idx],
            "confidence": confidence
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}


# ===============================
# 🔥 RETRAIN ENDPOINT
# ===============================
@app.post("/retrain")
async def retrain_model():
    """
    Retrains the model using images in retrain_data/ folder.
    Folder structure MUST be:
      retrain_data/
         Rock/
         Paper/
         Scissors/
    """
    try:
        DATA_DIR = "retrain_data"

        if not os.path.exists(DATA_DIR):
            return {"error": "retrain_data folder not found."}
        
        # Check if folder has subdirectories
        subdirs = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
        if len(subdirs) == 0:
            return {"error": "No class folders found in retrain_data/"}

        # Load dataset
        train_ds = tf.keras.utils.image_dataset_from_directory(
            DATA_DIR,
            image_size=(150, 150),
            batch_size=16,
            shuffle=True
        )

        # Normalization
        norm = tf.keras.layers.Rescaling(1./255)

        # Simple CNN
        new_model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(150, 150, 3)),
            norm,
            tf.keras.layers.Conv2D(32, 3, activation="relu"),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, activation="relu"),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(3, activation="softmax")
        ])

        new_model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )

        # Train 3 epochs
        history = new_model.fit(train_ds, epochs=3)

        # Export new SavedModel
        SAVE_PATH = "models/rps_model"
        new_model.export(SAVE_PATH)

        return {
            "message": "Model retrained successfully!",
            "epochs": 3,
            "samples_used": len(train_ds)
        }
    except Exception as e:
        return {"error": f"Retraining failed: {str(e)}"}
