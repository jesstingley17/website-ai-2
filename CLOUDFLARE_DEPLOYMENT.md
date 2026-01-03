# Cloudflare Deployment Guide

## Overview

This application has two parts:
1. **Frontend** (React + Vite) - ✅ Can deploy to **Cloudflare Pages**
2. **Backend** (FastAPI + Python) - ❌ **Cannot** deploy to Cloudflare (needs different platform)

## Recommended Architecture

```
Frontend (Cloudflare Pages)
    ↓ HTTPS/WebSocket
Backend (Railway/Render/Fly.io/etc.)
    ↓
Supabase (Database)
```

## Step 1: Deploy Frontend to Cloudflare Pages

### Option A: Via Cloudflare Dashboard

1. **Go to Cloudflare Dashboard**
   - Visit https://dash.cloudflare.com
   - Select your account
   - Go to **Pages** in the sidebar

2. **Create a New Project**
   - Click "Create a project"
   - Select "Connect to Git"
   - Connect your GitHub account and select `jesstingley17/website-ai-2`

3. **Configure Build Settings**
   - **Project name**: `lovable-clone` (or your preferred name)
   - **Production branch**: `main`
   - **Framework preset**: `Vite` (or None)
   - **Build command**: `cd frontend && npm install && npm run build`
   - **Build output directory**: `frontend/dist`
   - **Root directory**: Leave empty (or set to `/` if needed)

4. **Environment Variables**
   Add these in the Build settings:
   - `VITE_WS_URL` - Your backend WebSocket URL (e.g., `wss://your-backend.railway.app/ws`)
   - `VITE_BEAM_TOKEN` - Optional, if still using Beam auth

5. **Deploy**
   - Click "Save and Deploy"
   - Cloudflare will build and deploy your frontend
   - You'll get a URL like `https://lovable-clone.pages.dev`

### Option B: Via Wrangler CLI

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Navigate to frontend directory
cd frontend

# Build the frontend
npm install
npm run build

# Deploy to Cloudflare Pages
wrangler pages deploy dist --project-name=lovable-clone
```

## Step 2: Deploy Backend (Required - Can't Use Cloudflare)

Since Cloudflare Workers don't support Python/FastAPI, deploy the backend to one of these:

### Option A: Railway (Recommended - Easy)
1. Go to https://railway.app
2. Connect GitHub repo
3. Select `lovable-clone` directory
4. Set root directory to `/` (or create a `railway.json`)
5. Railway will auto-detect Python
6. Set environment variables:
   - All variables from `.env.example`
   - `PORT` will be auto-set by Railway
7. Deploy

**Railway Configuration File** (`railway.json`):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd /Users/jessica-leetingley/website-ai-2/lovable-clone && python -m src.server",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Option B: Render
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt && baml-cli generate`
   - **Start Command**: `python -m src.server`
   - **Environment**: Python 3
5. Add environment variables
6. Deploy

### Option C: Fly.io
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. `fly launch` in project root
3. Follow prompts
4. Deploy with `fly deploy`

### Option D: Heroku (if still using it)
Similar to Render setup.

## Step 3: Update Frontend Environment Variables

After deploying the backend, update your Cloudflare Pages environment variables:

1. Go to Cloudflare Pages → Your Project → Settings → Environment Variables
2. Add/Update:
   ```
   VITE_WS_URL=wss://your-backend.railway.app/ws
   ```
   (Replace with your actual backend URL)

3. Redeploy the frontend (or it will auto-redeploy on next git push)

## Step 4: Update Backend CORS

Update `src/server.py` to allow your Cloudflare Pages domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lovable-clone.pages.dev",  # Your Cloudflare Pages URL
        "https://yourdomain.com",  # Custom domain if you add one
        "http://localhost:5173",  # Local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Quick Start Commands

### Frontend Build (for Cloudflare Pages)
```bash
cd frontend
npm install
npm run build
# Output will be in frontend/dist/
```

### Backend Test (before deploying)
```bash
# Activate venv
source venv/bin/activate

# Set environment variables
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export SUPABASE_URL=...
# etc.

# Run server
python -m src.server
```

## Environment Variables Summary

### Frontend (Cloudflare Pages)
- `VITE_WS_URL` - Backend WebSocket URL (e.g., `wss://backend.railway.app/ws`)

### Backend (Railway/Render/etc.)
- All variables from `.env.example`:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `HOST=0.0.0.0`
  - `PORT` (usually auto-set by platform)

## Troubleshooting

### Frontend can't connect to backend
- Check CORS settings in `src/server.py`
- Verify `VITE_WS_URL` is set correctly
- Ensure backend is running and accessible
- Check WebSocket URL uses `wss://` (secure) not `ws://`

### Build fails on Cloudflare Pages
- Ensure `frontend/dist` exists after build
- Check build command is correct
- Verify `package.json` has all dependencies

### Backend deployment issues
- Ensure `requirements.txt` is up to date
- Check Python version (3.12+)
- Verify all environment variables are set
- Check platform logs for errors

## Alternative: Full Stack on One Platform

If you want everything in one place (not Cloudflare):
- **Render** - Can host both frontend and backend
- **Railway** - Can host both
- **Fly.io** - Can host both
- **Vercel** - Frontend + Serverless Functions (would need to rewrite backend)

## Next Steps

1. ✅ Deploy frontend to Cloudflare Pages
2. ✅ Deploy backend to Railway/Render/etc.
3. ✅ Update frontend environment variables
4. ✅ Update backend CORS settings
5. ✅ Test end-to-end

## References

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

