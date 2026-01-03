# Quick Start: Deploy Backend to Railway

## Why Railway?
- ✅ Free tier available
- ✅ Auto-detects Python
- ✅ Easy GitHub integration
- ✅ Automatic HTTPS
- ✅ Takes ~5 minutes to set up

## Step-by-Step

### 1. Sign Up
1. Go to https://railway.app
2. Sign up with GitHub (free)
3. Click "New Project"

### 2. Connect Repository
1. Select "Deploy from GitHub repo"
2. Choose your repository: `jesstingley17/website-ai-2`
3. Select branch: `main`
4. Railway will auto-detect Python

### 3. Configure (Optional)
Railway usually auto-detects everything, but you can verify:

**Settings → Variables:**
Add all your environment variables:
- `OPENAI_API_KEY` = your key
- `ANTHROPIC_API_KEY` = your key
- `SUPABASE_URL` = your URL
- `SUPABASE_SERVICE_ROLE_KEY` = your key
- `HOST` = `0.0.0.0` (Railway sets this automatically)
- `PORT` = (Railway sets this automatically)

**Settings → Deploy:**
- Root Directory: `/lovable-clone` (if needed)
- Build Command: `pip install -r requirements.txt && baml-cli generate`
- Start Command: `python -m src.server`

### 4. Deploy
1. Railway will automatically deploy
2. Wait for build to complete
3. Get your URL from the "Domains" tab
4. It will be something like: `https://your-app.railway.app`

### 5. Test
```bash
curl https://your-app.railway.app/health
# Should return: {"status":"ok"}
```

### 6. Update Cloudflare Pages
1. Go to Cloudflare Pages → Your Project → Settings → Environment Variables
2. Add: `VITE_WS_URL=wss://your-app.railway.app/ws`
3. Redeploy frontend

## That's It!

Your backend is now running on Railway, and your frontend on Cloudflare Pages will connect to it.

## Troubleshooting

**Build fails:**
- Check Railway logs
- Verify requirements.txt is correct
- Ensure Python version is compatible

**Server doesn't start:**
- Check Start Command: `python -m src.server`
- Verify all environment variables are set
- Check Railway logs for errors

**WebSocket connection fails:**
- Verify Railway URL is correct
- Check CORS settings in `src/server.py`
- Ensure WebSocket URL uses `wss://` (secure)

