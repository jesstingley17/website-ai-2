# Final Setup Steps

## ✅ Your Railway URL
**Backend URL**: `https://website-ai-2-production.up.railway.app`

## Step 1: Test Your Backend

Test that it's working:
```
https://website-ai-2-production.up.railway.app/health
```

Visit in browser or run:
```bash
curl https://website-ai-2-production.up.railway.app/health
```

Should return: `{"status":"ok"}`

## Step 2: Update Cloudflare Worker

### Option A: Using Cloudflare Dashboard (Easiest)

1. Go to https://dash.cloudflare.com
2. **Workers & Pages** → Click on `website` worker
3. **Settings** → **Variables**
4. Add/Edit variable:
   - **Name**: `BACKEND_URL`
   - **Value**: `https://website-ai-2-production.up.railway.app`
5. **Save**

### Option B: Using Wrangler CLI

```bash
cd worker
wrangler secret put BACKEND_URL
# Enter: https://website-ai-2-production.up.railway.app
```

## Step 3: Update Frontend Environment Variables

In Cloudflare Pages:

1. Go to **Cloudflare Dashboard** → **Pages**
2. Click on your project
3. **Settings** → **Environment Variables**
4. Add/Update these:

**For Production:**
```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

5. **Save** (or push a commit to trigger redeploy)

## Step 4: Test Everything

### Test 1: Backend Direct
```
https://website-ai-2-production.up.railway.app/health
```
Expected: `{"status":"ok"}`

### Test 2: Worker Proxy
```
https://website.jessicaleetingley.workers.dev/health
```
Expected: `{"status":"ok"}`

### Test 3: Frontend
- Visit your Cloudflare Pages URL
- Check browser console (F12)
- Should connect to backend without errors

## 🎉 Done!

Your architecture:
```
Frontend (Cloudflare Pages)
    ↓
Cloudflare Worker (website.jessicaleetingley.workers.dev)
    ↓
Backend (website-ai-2-production.up.railway.app)
    ↓
Supabase (Database)
```

## Quick Reference

- **Backend URL**: `https://website-ai-2-production.up.railway.app`
- **Health Check**: `https://website-ai-2-production.up.railway.app/health`
- **WebSocket**: `wss://website-ai-2-production.up.railway.app/ws`
- **Worker Proxy**: `https://website.jessicaleetingley.workers.dev`

