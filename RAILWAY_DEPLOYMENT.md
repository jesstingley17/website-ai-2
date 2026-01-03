# Deploy Python Backend to Railway - Step by Step

## Quick Overview

Railway will:
1. Detect your Python project
2. Install dependencies from `requirements.txt`
3. Run your FastAPI server
4. Give you a URL like `https://your-app.railway.app`

## Step 1: Sign Up / Login

1. Go to https://railway.app
2. Click "Start a New Project" or "Login"
3. Sign up with GitHub (recommended - it's free and easy)

## Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub (if first time)
4. Select your repository: `jesstingley17/website-ai-2`
5. Railway will detect it's a Python project automatically

## Step 3: Configure Project

Railway should auto-detect:
- **Language**: Python
- **Build Command**: `pip install -r requirements.txt && baml-cli generate`
- **Start Command**: `python -m src.server`

If it doesn't auto-detect, you can set:
- **Root Directory**: `/lovable-clone` (if needed)
- **Start Command**: `python -m src.server`

## Step 4: Set Environment Variables

This is the most important step! Add all your API keys:

1. In Railway dashboard, click on your project
2. Go to **"Variables"** tab
3. Click **"New Variable"** for each:

### Required Variables:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
HOST=0.0.0.0
```

### Optional Variables:

```
GOOGLE_API_KEY=... (if using Gemini)
DEBUG=false
PROJECTS_DIR=./projects
```

**Note:** Railway automatically sets `PORT` - you don't need to set it manually.

## Step 5: Deploy

1. Railway will automatically start deploying
2. Watch the build logs
3. Wait for "Deployment successful"
4. Click on the deployment to see logs

## Step 6: Get Your URL

1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. You'll get a URL like: `https://your-app.railway.app`
4. Copy this URL - you'll need it!

## Step 7: Test Your Backend

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Should return: {"status":"ok"}
```

## Step 8: Update Worker Configuration

Now update your Cloudflare Worker to point to Railway:

```bash
cd worker
wrangler secret put BACKEND_URL
# Enter: https://your-app.railway.app
```

Or set it in Cloudflare Dashboard:
- Workers & Pages → Your Worker → Settings → Variables
- Add: `BACKEND_URL` = `https://your-app.railway.app`

## Step 9: Update Frontend

In Cloudflare Pages → Settings → Environment Variables:

```
VITE_WS_URL=wss://your-app.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

## Troubleshooting

### Build Fails

**Error: "Module not found"**
- Check `requirements.txt` is correct
- Verify all dependencies are listed

**Error: "BAML not found"**
- Build command should include: `baml-cli generate`
- Check `baml-cli` is in requirements.txt (it comes with `baml-py`)

### Server Won't Start

**Error: "Port already in use"**
- Remove `PORT` from environment variables (Railway sets it automatically)

**Error: "Missing environment variable"**
- Check all required variables are set in Railway
- Check variable names match exactly (case-sensitive)

### Database Connection Fails

**Error: "Supabase connection failed"**
- Verify `SUPABASE_URL` is correct
- Check `SUPABASE_SERVICE_ROLE_KEY` is set (not anon key)
- Test Supabase connection from local machine first

### WebSocket Not Working

**Connection refused**
- Ensure Railway deployment is running
- Check URL uses `wss://` (secure) not `ws://`
- Verify WebSocket endpoint exists: `/ws`

## Monitoring

- **Logs**: Click on deployment → "View Logs"
- **Metrics**: Railway dashboard shows CPU, memory usage
- **Restarts**: Railway automatically restarts on failure

## Costs

- **Free tier**: $5 credit/month (usually enough for development)
- **After free tier**: Pay-as-you-go (very affordable for small projects)

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Test backend is running
3. ✅ Update Worker BACKEND_URL
4. ✅ Update frontend environment variables
5. ✅ Test full stack integration

## Quick Reference

**Railway URL**: `https://your-app.railway.app`
**Health Check**: `https://your-app.railway.app/health`
**WebSocket**: `wss://your-app.railway.app/ws`

**Worker Proxy**: `https://website.jessicaleetingley.workers.dev`
**Frontend**: Your Cloudflare Pages URL

