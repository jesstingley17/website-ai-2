# Troubleshooting "Connecting to Workspace..." Message

## The Problem

Your frontend is loading but stuck on "Connecting to Workspace..." - this means it can't connect to your backend.

## Quick Checklist

### 1. Check Environment Variables

In Cloudflare Pages → Settings → Environment Variables, make sure you have:

```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

**Important:** After adding variables, Pages needs to rebuild. Either:
- Push a commit to trigger rebuild, OR
- Go to Deployments → Retry latest deployment

### 2. Check Backend is Running

Test your backend directly:

```bash
curl https://website-ai-2-production.up.railway.app/health
```

Should return: `{"status":"ok"}`

If not, check Railway logs - backend might have crashed.

### 3. Check Worker Configuration

In Cloudflare Worker → Settings → Variables:

Make sure `BACKEND_URL` is set:
```
BACKEND_URL=https://website-ai-2-production.up.railway.app
```

Test Worker:

```bash
curl https://website.jessicaleetingley.workers.dev/health
```

Should return: `{"status":"ok"}`

### 4. Check Browser Console

1. Open your site: https://website-ai-2.pages.dev
2. Press F12 (open DevTools)
3. Go to Console tab
4. Look for errors (red text)

Common errors:
- `WebSocket connection failed`
- `Network error`
- `CORS error`
- `Environment variable not defined`

### 5. Verify WebSocket Endpoint

Test WebSocket directly:

```bash
# Test if WebSocket endpoint exists
curl https://website-ai-2-production.up.railway.app/ws
```

Or check in browser console:

```javascript
const ws = new WebSocket('wss://website-ai-2-production.up.railway.app/ws');
ws.onopen = () => console.log('Connected!');
ws.onerror = (e) => console.error('Error:', e);
```

## Common Issues & Fixes

### Issue 1: Environment Variables Not Set

**Symptom:** Console shows `VITE_WS_URL is undefined`

**Fix:**
1. Add variables in Cloudflare Pages
2. Redeploy (push commit or retry deployment)
3. Variables are baked into build, so rebuild is required

### Issue 2: Backend Not Running

**Symptom:** Connection timeout or 502 error

**Fix:**
1. Check Railway logs
2. Verify backend is running
3. Check all environment variables are set in Railway

### Issue 3: CORS Errors

**Symptom:** Browser console shows CORS errors

**Fix:**
1. Update `src/server.py` CORS settings
2. Add your Pages URL to `allow_origins`
3. Redeploy backend to Railway

### Issue 4: WebSocket Connection Failed

**Symptom:** WebSocket errors in console

**Fix:**
1. Verify URL uses `wss://` (secure WebSocket)
2. Check backend WebSocket endpoint is working
3. Verify backend is accessible

## Step-by-Step Debugging

1. **Check backend health:**
   ```bash
   curl https://website-ai-2-production.up.railway.app/health
   ```

2. **Check browser console:**
   - Open DevTools (F12)
   - Look for errors
   - Check Network tab for failed requests

3. **Verify environment variables:**
   - Check Pages → Settings → Variables
   - Make sure they're set for Production
   - Redeploy if you just added them

4. **Check Worker:**
   ```bash
   curl https://website.jessicaleetingley.workers.dev/health
   ```

5. **Test WebSocket:**
   - Use browser console WebSocket test (see above)

## Quick Fix Steps

1. ✅ Add environment variables to Cloudflare Pages
2. ✅ Redeploy frontend (push commit or retry)
3. ✅ Verify backend is running on Railway
4. ✅ Check browser console for specific errors
5. ✅ Test backend endpoints directly

Share what you see in the browser console and we can fix the specific issue!

