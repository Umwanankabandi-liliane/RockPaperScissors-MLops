import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory

# Load the dataset
train_ds = image_dataset_from_directory(
    "data/train",
    image_size=(150,150),
    batch_size=32
)

val_ds = image_dataset_from_directory(
    "data/test",
    image_size=(150,150),
    batch_size=32
)

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(150,150,3)),
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train
model.fit(train_ds, validation_data=val_ds, epochs=5)

# Save model
model.save("models/rps_model.h5", save_format="h5")

print("Model saved successfully!")
