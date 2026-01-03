# Fix: Stuck on "Connecting to Workspace..."

## The Problem

The frontend is trying to connect to your backend via WebSocket but failing.

## Step-by-Step Fix

### Step 1: Check Environment Variables

**Have you added environment variables to Cloudflare Pages?**

1. Go to Cloudflare Dashboard → Pages → `website-ai-2`
2. Settings → Environment Variables
3. Make sure you have (as TEXT, not secrets):

```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

**If you just added them:**
- Variables are baked into the build
- You MUST redeploy after adding variables
- Push a commit OR retry the deployment

### Step 2: Check Browser Console

1. Open your site: https://website-ai-2.pages.dev/create
2. Press F12 (DevTools)
3. Go to Console tab
4. Look for WebSocket errors

Common errors:
- `WebSocket connection failed`
- `VITE_WS_URL is undefined`
- `Network error`
- Connection timeout

### Step 3: Verify Backend is Running

Test your backend:

```bash
curl https://website-ai-2-production.up.railway.app/health
```

Should return: `{"status":"ok"}`

If not, check Railway logs - backend might have crashed.

### Step 4: Test WebSocket Endpoint

In browser console, test WebSocket:

```javascript
const ws = new WebSocket('wss://website-ai-2-production.up.railway.app/ws');
ws.onopen = () => console.log('✅ WebSocket connected!');
ws.onerror = (e) => console.error('❌ WebSocket error:', e);
ws.onclose = (e) => console.log('WebSocket closed:', e.code, e.reason);
```

### Step 5: Redeploy Frontend

After adding/changing environment variables:

**Option A: Push a commit**
```bash
# Make a small change and push
git commit --allow-empty -m "Trigger rebuild with env vars"
git push
```

**Option B: Retry deployment**
1. Cloudflare Dashboard → Pages → `website-ai-2`
2. Deployments tab
3. Click on latest deployment
4. Click "Retry deployment"

## Most Common Issue

**Environment variables not set or frontend not rebuilt**

1. ✅ Add variables to Cloudflare Pages
2. ✅ Redeploy (push commit or retry)
3. ✅ Variables get baked into build
4. ✅ WebSocket connection works

## Quick Checklist

- [ ] Environment variables added to Cloudflare Pages
- [ ] Frontend redeployed after adding variables
- [ ] Backend is running on Railway
- [ ] Checked browser console for errors
- [ ] WebSocket URL is correct (`wss://` not `ws://`)

## Next Steps

1. **Add environment variables** (if not done)
2. **Redeploy frontend** (critical!)
3. **Check browser console** for specific errors
4. **Test backend** is accessible

Share what you see in the browser console and we can fix it!

