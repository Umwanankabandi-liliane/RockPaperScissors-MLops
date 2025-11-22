# Rock-Paper-Scissors MLOps System

🎯 Complete MLOps pipeline for Rock-Paper-Scissors image classification with FastAPI, Streamlit, and automated retraining.

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Umwanankabandi-liliane/RockPaperScissors-MLops.git
cd RockPaperScissors-MLops
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get the trained model
**⚠️ IMPORTANT:** Model files are NOT in the repo (too large for GitHub).

**Option A:** Train your own model (Recommended)
```bash
python train_model.py
```

**Option B:** Download pre-trained model
- Download from: [Google Drive Link - TO BE ADDED]
- Extract to `models/` folder

### 4. Run the application

**Backend (FastAPI):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Streamlit):**
```bash
streamlit run app.py
```

Visit: http://localhost:8501

## 1. Project Overview

This repository contains all components required to build, deploy, and retrain an image classifier:

* ✅ Train Rock-Paper-Scissors classifier using TensorFlow
* ✅ FastAPI backend with prediction & retraining endpoints
* ✅ Streamlit UI for predictions and bulk uploads
* ✅ Model evaluation with multiple metrics
* ✅ Load testing with Locust
* ✅ Docker deployment ready


## 3. Model Training

The model is trained using a TensorFlow pipeline and exported as a TensorFlow SavedModel directory.

Training steps included:

1. Loading the Rock-Paper-Scissors dataset.
2. Preprocessing and resizing images to 150×150 pixels.
3. Building a CNN classifier.
4. Training for several epochs.
5. Exporting the model using `model.export("models/rps_model")`.

The exported directory is used by FastAPI for inference.


## 4. FastAPI Service

The FastAPI backend provides two main endpoints:

### **POST /predict**

Accepts an image file and returns:

* Predicted class (Rock, Paper, or Scissors)
* Confidence score

### **POST /retrain**

Retrains the model using images placed inside the `retrain_data/` directory.
The folder must contain the following structure:


retrain_data/
├── rock/
├── paper/
└── scissors/


After retraining, the updated model replaces the previous one inside `models/`.



## 5. Streamlit Interface

The Streamlit application allows users to:

* Upload an image and receive a model prediction.
* Trigger model retraining directly from the UI.

Streamlit communicates with the FastAPI backend through HTTP requests.

To launch Streamlit:


streamlit run app.py


Ensure the FastAPI server is running before using the UI:


uvicorn main:app --reload




## 6. Technologies Used

* Python 3.10
* TensorFlow and Keras
* FastAPI
* Streamlit
* NumPy and Pillow
* Uvicorn



## 7. How to Run the System Locally

### Step 1: Install dependencies


pip install -r requirements.txt


### Step 2: Start FastAPI


uvicorn main:app --reload


### Step 3: Start Streamlit UI


streamlit run app.py


### Step 4: Open the UI

Go to:


http://localhost:8501


Swagger documentation is available at:


http://127.0.0.1:8000/docs




## 8. Retraining Instructions

To retrain the model:

1. Place new images into `retrain_data/rock`, `retrain_data/paper`, and `retrain_data/scissors`.
2. Call the `/retrain` endpoint from Swagger or from Streamlit.
3. The model will be retrained and saved automatically.



## 9. Notebook

The `notebook/` directory contains the full analysis for Task 1, including:

* Understanding the dataset
* Preprocessing and augmentation
* Model architecture
* Evaluation and export

This notebook forms part of the assessment deliverables.



## 10. License

This project is developed for academic purposes and is free for educational use.




