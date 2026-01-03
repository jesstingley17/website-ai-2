# Next Steps - Connect Everything Together

## ✅ What's Done
- Backend is online on Railway!

## 🎯 What's Next

### Step 1: Get Your Railway URL

1. In Railway dashboard, click on your service
2. Go to **Settings** → **Networking**
3. You should see a domain like: `https://your-app.railway.app`
4. **Copy this URL** - you'll need it!

### Step 2: Test Your Backend

Test that your backend is working:
```bash
curl https://your-app.railway.app/health
```

Or visit in browser: `https://your-app.railway.app/health`

Should return: `{"status":"ok"}`

### Step 3: Update Cloudflare Worker

Connect your Worker to the Railway backend:

**Option A: Using Wrangler CLI**
```bash
cd worker
wrangler secret put BACKEND_URL
# When prompted, enter: https://your-app.railway.app
```

**Option B: Using Cloudflare Dashboard**
1. Go to https://dash.cloudflare.com
2. **Workers & Pages** → Your Worker (`website`)
3. **Settings** → **Variables**
4. Click **"Add Variable"** or edit existing:
   - Name: `BACKEND_URL`
   - Value: `https://your-app.railway.app`
5. Save

### Step 4: Update Frontend Environment Variables

In Cloudflare Pages:

1. Go to **Cloudflare Dashboard** → **Pages**
2. Click on your project
3. **Settings** → **Environment Variables**
4. Add/Update these variables:

**For Production:**
```
VITE_WS_URL=wss://your-app.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

**For Preview (optional):**
```
VITE_WS_URL=wss://your-app.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

5. **Redeploy** the frontend (or push a commit to trigger redeploy)

### Step 5: Update Backend CORS (If Needed)

If you get CORS errors, update `src/server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.pages.dev",  # Your Cloudflare Pages URL
        "https://website.jessicaleetingley.workers.dev",  # Worker URL
        "http://localhost:5173",  # Local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy to Railway.

### Step 6: Test Everything

1. **Test Backend Direct:**
   - Visit: `https://your-app.railway.app/health`
   - Should see: `{"status":"ok"}`

2. **Test Worker Proxy:**
   - Visit: `https://website.jessicaleetingley.workers.dev/health`
   - Should see: `{"status":"ok"}`

3. **Test Frontend:**
   - Visit your Cloudflare Pages URL
   - Check browser console for errors
   - Test WebSocket connection

## 🎉 Summary

Your architecture is now:
```
Frontend (Cloudflare Pages)
    ↓
Cloudflare Worker (Proxy)
    ↓
Backend (Railway)
    ↓
Supabase (Database)
```

## 🔍 Troubleshooting

### Worker returns 502
- Check `BACKEND_URL` is set correctly in Worker
- Verify backend is running on Railway
- Check Railway logs

### Frontend can't connect
- Check environment variables are set
- Verify WebSocket URL uses `wss://` (secure)
- Check browser console for errors

### CORS errors
- Update CORS settings in `src/server.py`
- Redeploy backend to Railway

### WebSocket not working
- Use direct connection: `wss://your-app.railway.app/ws`
- Check backend logs for WebSocket errors

## ✅ Final Checklist

- [ ] Railway backend is online
- [ ] Test `/health` endpoint works
- [ ] Worker `BACKEND_URL` is set
- [ ] Frontend environment variables are set
- [ ] Frontend is redeployed
- [ ] Everything is tested!

