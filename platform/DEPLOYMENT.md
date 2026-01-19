# Deployment Guide

## Quick Overview

This platform has two parts:

- **Frontend**: Static HTML/JS/CSS (can deploy to Vercel, Netlify, GitHub Pages)
- **Backend**: Python FastAPI (needs Railway, Render, or Fly.io)

---

## Option 1: Deploy Backend to Railway (Free Tier)

### Step 1: Push to GitHub

```bash
cd /home/user/Desktop/traffic_analysis
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/traffic-analytics.git
git push -u origin main
```

### Step 2: Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python
6. Set the **Root Directory** to `platform/backend`
7. Add these environment variables:
   - `PORT`: `8000`
8. Railway will auto-deploy!
9. Copy your backend URL (e.g., `https://traffic-analytics-backend.up.railway.app`)

### Step 3: Update Frontend API URL

Edit `platform/frontend/js/app.js`:

```javascript
const API_BASE = "https://YOUR-RAILWAY-URL.up.railway.app/api";
```

### Step 4: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "Add New" → "Project"
4. Select your repository
5. Set **Root Directory** to `platform/frontend`
6. Click "Deploy"

---

## Option 2: Deploy Everything to Render.com

Render supports both frontend and backend in one place.

### Step 1: Create render.yaml

```yaml
services:
  - type: web
    name: traffic-analytics-backend
    runtime: python
    rootDir: platform/backend
    buildCommand: pip install -r ../requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"

  - type: web
    name: traffic-analytics-frontend
    runtime: static
    rootDir: platform/frontend
    buildCommand: echo "No build needed"
    staticPublishPath: .
```

### Step 2: Deploy

1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Create new "Blueprint" and select your repo
4. Render will deploy both services

---

## Option 3: Docker Deployment (DigitalOcean, AWS, etc.)

Use the Dockerfile for containerized deployment.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY platform/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY platform/backend ./backend

# Copy frontend (served by FastAPI)
COPY platform/frontend ./frontend

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Files You Need for Deployment

### platform/backend/requirements.txt

Already exists with:

- fastapi
- uvicorn
- pandas
- plotly
- etc.

### Procfile (for Heroku/Railway)

```
web: cd platform/backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Environment Variables

- `PORT`: Server port (usually auto-set)
- No other secrets required for basic deployment

## CORS Configuration

The backend already has CORS configured to allow all origins (`*`). For production, update `main.py` to restrict origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
