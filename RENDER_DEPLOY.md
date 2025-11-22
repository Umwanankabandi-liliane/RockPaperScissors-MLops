# Render Deployment Guide

## 🚀 Quick Deploy to Render

### Step 1: Push to GitHub

First, commit everything:
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `Umwanankabandi-liliane/RockPaperScissors-MLops`

### Step 3: Configure Service

**Basic Settings:**
- **Name:** `rps-mlops`
- **Region:** Choose closest to you
- **Branch:** `main`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:**
```bash
pip install -r requirements.txt && python build.py
```

- **Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
- Start with **Free** (will be slow for model training)
- Upgrade to **Starter ($7/month)** for better performance

### Step 4: Environment Variables (Optional)

Add if needed:
- `PYTHON_VERSION=3.10.0`

### Step 5: Deploy!

Click **"Create Web Service"**

Render will:
1. ✅ Install dependencies
2. ✅ Run `build.py` (downloads/trains model automatically)
3. ✅ Start FastAPI server
4. ✅ Provide public URL

## 📱 Access Your App

After deployment (5-10 minutes):
- **API:** `https://rps-mlops.onrender.com`
- **Docs:** `https://rps-mlops.onrender.com/docs`

## 🎨 Deploy Streamlit UI (Separate Service)

Create another web service:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Update `FASTAPI_URL` in `app.py` to your FastAPI URL.

## ⚡ Important Notes

1. **First deployment is slow** (builds model from scratch ~5-10 min)
2. **Free tier sleeps** after 15 min of inactivity
3. **Model persists** - only trains once during first deployment
4. **Upgrade to Starter** for production use

## 🐛 Troubleshooting

**Build fails:**
- Check build logs in Render dashboard
- Ensure all dependencies in requirements.txt

**Model not found:**
- `build.py` should run automatically
- Check build logs for errors

**Timeout during build:**
- Upgrade to paid plan (more build time)

## 🔄 Alternative: Deploy with Docker

If you prefer Docker on Render:

**Dockerfile:** Already created
**Start Command:** Leave blank (uses Dockerfile CMD)

Render will use your Dockerfile automatically.
