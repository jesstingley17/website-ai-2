# Get Your Public Railway URL

## The Issue

`website-ai-2.railway.internal` is an **internal domain** - it only works inside Railway's network, not from the internet.

You need a **public domain** to connect from Cloudflare Worker and your frontend.

## How to Get a Public URL

### Step 1: Generate Public Domain

1. In Railway dashboard, click on your service
2. Go to **Settings** → **Networking** (or **Domains**)
3. Look for **"Generate Domain"** button
4. Click it
5. Railway will create a public domain like:
   - `https://website-ai-2-production-xxxx.up.railway.app`
   - OR `https://website-ai-2.up.railway.app`

### Step 2: Copy the Public URL

Once generated, you'll see something like:
```
https://website-ai-2-production-xxxx.up.railway.app
```

**This is the URL you need!**

## Alternative: Use Custom Domain

If you have a custom domain:
1. Go to **Settings** → **Networking**
2. Click **"Custom Domain"**
3. Add your domain
4. Railway will give you DNS records to add

## What to Do With the Public URL

Once you have the public URL (e.g., `https://website-ai-2-production-xxxx.up.railway.app`):

### 1. Test It
Visit in browser:
```
https://website-ai-2-production-xxxx.up.railway.app/health
```
Should return: `{"status":"ok"}`

### 2. Update Cloudflare Worker
Set `BACKEND_URL` to your public Railway URL:
```
BACKEND_URL=https://website-ai-2-production-xxxx.up.railway.app
```

### 3. Update Frontend
Set environment variable:
```
VITE_WS_URL=wss://website-ai-2-production-xxxx.up.railway.app/ws
```

## Quick Checklist

- [ ] Generate public domain in Railway
- [ ] Test `/health` endpoint works
- [ ] Copy the public URL
- [ ] Update Worker `BACKEND_URL`
- [ ] Update frontend `VITE_WS_URL`

