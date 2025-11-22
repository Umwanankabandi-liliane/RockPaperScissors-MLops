"""
Build script for Render deployment.
This runs during build phase to set up the model.
"""
import os
import sys

print("=" * 50)
print("RENDER BUILD SCRIPT STARTING")
print("=" * 50)

# Check if model exists
model_path = "models/rps_model"
h5_model_path = "models/rps_model.h5"

if os.path.exists(model_path) or os.path.exists(h5_model_path):
    print("✅ Model already exists, skipping training")
    sys.exit(0)

print("🔨 No model found, training new model...")

# Check if training data exists
if not os.path.exists("data/train"):
    print("⚠️  No training data found - will download from TensorFlow datasets")
    
    # Create simple model using tensorflow_datasets
    import tensorflow_datasets as tfds
    import tensorflow as tf
    
    print("📥 Loading Rock Paper Scissors dataset...")
    (train_ds, test_ds), ds_info = tfds.load(
        'rock_paper_scissors',
        split=['train', 'test'],
        as_supervised=True,
        with_info=True
    )
    
    print(f"✅ Dataset loaded: {ds_info}")
    
    # Preprocessing
    IMG_SIZE = 150
    BATCH_SIZE = 32
    
    def preprocess(image, label):
        image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
        image = image / 255.0
        return image, label
    
    train = train_ds.map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    test = test_ds.map(preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    
    # Build lightweight model
    print("🏗️  Building model...")
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(150, 150, 3)),
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(3, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("🎯 Training model (5 epochs)...")
    model.fit(train, validation_data=test, epochs=5, verbose=2)
    
    # Save model
    os.makedirs("models", exist_ok=True)
    print("💾 Saving model...")
    model.export("models/rps_model")
    
    print("✅ Model trained and saved successfully!")
    
else:
    print("📚 Training data found locally, running train_model.py...")
    import subprocess
    subprocess.run([sys.executable, "train_model.py"], check=True)
    print("✅ Model training complete!")

print("=" * 50)
print("BUILD SCRIPT COMPLETED SUCCESSFULLY")
print("=" * 50)
