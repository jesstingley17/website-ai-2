# Fixing "Connecting to Workspace..." Issue

If you're stuck on "Connecting to Workspace...", the WebSocket connection is failing. Follow these steps:

## Step 1: Check Browser Console

1. Open your site: https://website-ai-2.pages.dev/create
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Look for errors (red text)

**Common errors you might see:**
- `WebSocket connection failed`
- `VITE_WS_URL is undefined`
- `Failed to connect`
- Connection timeout errors

## Step 2: Verify Environment Variables in Cloudflare Pages

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to **Pages** → Your project
3. Go to **Settings** → **Environment Variables**
4. Check that you have:

```
VITE_WS_URL = wss://website-ai-2-production.up.railway.app/ws
```

**Important notes:**
- Must use `wss://` (secure WebSocket), NOT `ws://`
- Must include `/ws` at the end
- Make sure it's set for **Production** environment
- After setting, you need to **redeploy** (trigger a new build)

## Step 3: Verify Backend is Running

Test if your backend is accessible:

1. Open: https://website-ai-2-production.up.railway.app/health
2. You should see: `{"status":"ok"}`

If you see an error or timeout, your backend isn't running. Check Railway logs.

## Step 4: Check Backend Logs on Railway

1. Go to [Railway Dashboard](https://railway.app)
2. Open your project
3. Click on your service
4. Go to **Deployments** → Click latest deployment → **View Logs**
5. Look for:
   - Server starting messages
   - Any error messages
   - WebSocket connection attempts

## Step 5: Trigger a Rebuild

After setting/changing environment variables:

1. Go to Cloudflare Pages dashboard
2. Go to **Deployments**
3. Click **Retry deployment** on the latest deployment
   - OR make an empty commit and push:
     ```bash
     git commit --allow-empty -m "Trigger rebuild"
     git push
     ```

## Step 6: Test the WebSocket Connection Directly

Open your browser console (F12) and run:

```javascript
const ws = new WebSocket('wss://website-ai-2-production.up.railway.app/ws');
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.error('Error:', e);
ws.onclose = (e) => console.log('Closed:', e.code, e.reason);
```

- If it connects: Backend is working, issue is with frontend config
- If it fails: Backend WebSocket endpoint has an issue

## Common Issues

### Issue 1: Environment Variable Not Set
**Symptom:** Console shows `VITE_WS_URL is undefined`
**Fix:** Set `VITE_WS_URL` in Cloudflare Pages environment variables

### Issue 2: Wrong URL Format
**Symptom:** Connection fails immediately
**Fix:** Ensure URL is `wss://` not `ws://`, and includes `/ws`

### Issue 3: Backend Not Running
**Symptom:** Health check fails or WebSocket connection times out
**Fix:** Check Railway deployment and logs

### Issue 4: CORS Issues
**Symptom:** Connection blocked by browser
**Fix:** Backend should already have CORS configured, but verify in `src/server.py`

### Issue 5: Environment Variable Not Applied
**Symptom:** Variable is set but still not working
**Fix:** Variables only apply to NEW builds. Trigger a rebuild after setting variables.

## Quick Checklist

- [ ] `VITE_WS_URL` is set in Cloudflare Pages (Production environment)
- [ ] URL format: `wss://website-ai-2-production.up.railway.app/ws`
- [ ] Backend health check works: https://website-ai-2-production.up.railway.app/health
- [ ] Backend logs show server is running
- [ ] Triggered a rebuild after setting environment variables
- [ ] Browser console shows connection attempts/errors
- [ ] No firewall/network blocking WebSocket connections

## Next Steps

If none of these work, share:
1. What errors you see in the browser console
2. What `VITE_WS_URL` is set to in Cloudflare Pages
3. Whether the backend health check works
4. Any errors from Railway logs
