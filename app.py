import streamlit as st
import requests
from PIL import Image
import io

# =========================
# CONFIG
# =========================
FASTAPI_URL = "https://rockpaperscissors-mlops-7.onrender.com"  # Your FastAPI backend URL

st.set_page_config(page_title="Rock Paper Scissors Classifier", layout="centered")

st.title("🪨📄✂️ Rock-Paper-Scissors Classifier")
st.write("Upload an image and let the ML model predict!")

# =========================
# IMAGE UPLOAD + PREDICT
# =========================
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=250)

    if st.button("🔍 Predict"):
        # Send image to FastAPI
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "image/png")}
        response = requests.post(f"{FASTAPI_URL}/predict", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success(f"Prediction: **{data['prediction']}**")
            st.info(f"Confidence: **{data['confidence']:.2f}**")
        else:
            st.error("Prediction failed. Check FastAPI logs.")

# =========================
# RETRAIN BUTTON
# =========================
st.write("---")
st.header("🔁 Retrain Model")

st.write("Click below to retrain the model using new images inside `retrain_data/`.")

if st.button("🔧 Retrain Model"):
    response = requests.post(f"{FASTAPI_URL}/retrain")

    if response.status_code == 200:
        st.success("Retraining completed!")
        st.json(response.json())
    else:
        st.error("Retrain request failed.")
