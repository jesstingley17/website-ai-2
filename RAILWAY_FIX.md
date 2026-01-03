# Railway Deployment Fix - Start Command Not Found

## The Problem

Railway can't find the start command because it's looking at the repo root, but your code is in the `lovable-clone/` directory.

## Quick Fix - Set in Railway Dashboard

### Option 1: Set Root Directory + Start Command (Recommended)

1. In Railway dashboard, click on your project
2. Go to **Settings** → **Service**
3. Set **Root Directory**: `lovable-clone`
4. Set **Start Command**: `python -m src.server`
5. Click **Save**
6. Railway will redeploy automatically

### Option 2: Use Procfile (Already Created)

I've created a `Procfile` in the `lovable-clone/` directory. Railway will use it if:
- Root Directory is set to `lovable-clone`, OR
- You push the Procfile to your repo and Railway detects it

## Step-by-Step Fix

### In Railway Dashboard:

1. **Click on your project/deployment**
2. **Go to "Settings"** (gear icon)
3. **Click on "Service"** tab
4. **Set Root Directory:**
   - Value: `lovable-clone`
5. **Set Start Command:**
   - Value: `python -m src.server`
6. **Set Build Command (optional but recommended):**
   - Value: `pip install -r requirements.txt && baml-cli generate`
7. **Click "Save"**
8. Railway will automatically redeploy

## Verify It Works

After saving, check the deployment logs. You should see:
- ✅ Dependencies installing
- ✅ Server starting
- ✅ "Application startup complete"
- ✅ "Uvicorn running on http://0.0.0.0:PORT"

## Test Your Backend

Once deployed, test the health endpoint:
```
https://your-app.railway.app/health
```

Should return: `{"status":"ok"}`

## Alternative: Move Files to Repo Root

If you prefer, you could move everything from `lovable-clone/` to the repo root, but that's more work and the above solution is easier.

