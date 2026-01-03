# Debugging 502 Error - Application Failed to Respond

## The Problem

Your backend URL is accessible, but Railway returns:
```json
{"status":"error","code":502,"message":"Application failed to respond"}
```

This means:
- ✅ Railway is running
- ✅ Network is accessible
- ❌ Your Python application isn't responding

## Common Causes

### 1. Server Not Starting
- Application crashed on startup
- Missing environment variables
- Python errors in code

### 2. Wrong Port
- Application listening on wrong port
- Railway sets PORT automatically (check environment)

### 3. Application Error
- Configuration errors
- Database connection failures
- Import errors

## How to Debug

### Step 1: Check Railway Logs

1. Go to Railway dashboard
2. Click on your service
3. Go to **"Deployments"** tab
4. Click on the latest deployment
5. Click **"View Logs"**
6. Look for errors (red text)

### Step 2: Check for Common Errors

Look in logs for:
- `Configuration errors: ...` (missing env vars)
- `ModuleNotFoundError` (missing dependencies)
- `Connection refused` (database issues)
- `ValueError` (config problems)

### Step 3: Verify Environment Variables

Make sure all required variables are set:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `HOST=0.0.0.0`

**Important**: Don't set `PORT` - Railway sets it automatically!

### Step 4: Check Start Command

In Railway → Settings → Service:
- **Start Command**: `python -m src.server`
- **Root Directory**: `lovable-clone`

## Quick Fixes

### If Missing Environment Variables

1. Go to Railway → Variables
2. Add all required variables
3. Railway will redeploy automatically

### If Server Crashes on Startup

Check logs for the specific error:
- Database connection issues → Check Supabase credentials
- Config validation errors → Check all env vars are set
- Import errors → Check requirements.txt includes everything

### If Port Issues

The server should use the PORT from environment:
```python
PORT = int(os.getenv("PORT", "8000"))
```

Railway automatically sets `PORT` - don't set it manually!

## What to Look For in Logs

Good logs should show:
```
Agent initialized
Application startup complete
Uvicorn running on http://0.0.0.0:PORT
```

Bad logs might show:
```
Configuration errors: OPENAI_API_KEY is required
ValueError: ...
ConnectionError: ...
ModuleNotFoundError: ...
```

## Next Steps

1. Check Railway logs (most important!)
2. Share the error message from logs
3. Fix the specific issue
4. Redeploy

Share what you see in the Railway logs and I can help fix the specific error!

