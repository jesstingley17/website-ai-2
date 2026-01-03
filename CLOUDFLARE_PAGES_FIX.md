# Fix: Cloudflare Pages Configuration

## The Problem

You're seeing the Python server start in Cloudflare Pages, but **Cloudflare Pages cannot run Python servers**. It's for static sites only.

The server starts during the build, but then the build process ends and the server stops. This won't work for your application.

## The Solution

### For Cloudflare Pages (Frontend Only)

**Build Settings:**
- **Build command**: `cd frontend && npm install && npm run build`
- **Build output directory**: `frontend/dist`
- **Deploy command**: (Leave empty or remove it)
- **Root directory**: (Leave empty)

**DO NOT** set a deploy command that runs `python -m src.server` - Cloudflare Pages cannot keep servers running.

### For Backend (Deploy Separately)

You **must** deploy your Python backend to a different platform:

**Option 1: Railway** (Easiest)
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repository
4. Add environment variables (from `.env.example`)
5. Railway auto-detects Python and runs your server

**Option 2: Render**
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build: `pip install -r requirements.txt && baml-cli generate`
5. Start: `python -m src.server`
6. Add environment variables

**Option 3: Fly.io**
1. Install flyctl
2. Run `fly launch` in your project
3. Deploy with `fly deploy`

## Correct Architecture

```
┌─────────────────────────────────┐
│  Cloudflare Pages (Frontend)    │
│  - React/Vite static site       │
│  - Build command only           │
│  - NO deploy command            │
└──────────────┬──────────────────┘
               │ HTTPS/WebSocket
               ↓
┌─────────────────────────────────┐
│  Railway/Render/Fly.io (Backend)│
│  - Python/FastAPI server        │
│  - WebSocket support            │
│  - Runs continuously            │
└──────────────┬──────────────────┘
               │
               ↓
┌─────────────────────────────────┐
│  Supabase (Database)            │
└─────────────────────────────────┘
```

## Steps to Fix

1. **In Cloudflare Pages Dashboard:**
   - Go to your project settings
   - Remove/clear the "Deploy command" field (or set it to empty)
   - Keep only the build command: `cd frontend && npm install && npm run build`
   - Set build output directory: `frontend/dist`

2. **Deploy Backend Separately:**
   - Choose Railway, Render, or Fly.io
   - Deploy your Python backend there
   - Get the backend URL (e.g., `https://your-app.railway.app`)

3. **Update Frontend Environment Variables:**
   - In Cloudflare Pages → Settings → Environment Variables
   - Add: `VITE_WS_URL=wss://your-backend-url.railway.app/ws`
   - Replace with your actual backend URL

4. **Update Backend CORS:**
   - Edit `src/server.py`
   - Add your Cloudflare Pages URL to `allow_origins`

## Quick Fix Summary

**Cloudflare Pages Settings:**
```
Build command: cd frontend && npm install && npm run build
Build output: frontend/dist
Deploy command: (EMPTY - remove it!)
```

**Backend:** Deploy to Railway/Render/Fly.io separately

