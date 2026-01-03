# Environment Variables Set But Not Working

## The Problem

You've set the environment variables, but the connection still fails.

## Most Likely Cause

**Frontend wasn't rebuilt after adding variables.**

Environment variables are baked into the build at build time. Just adding them doesn't update the deployed site - you need to rebuild.

## Check If Variables Are Actually Being Used

### Method 1: Check Browser Console

1. Open your site: https://website-ai-2.pages.dev/create
2. Press F12 → Console
3. Type this in console:

```javascript
console.log('WS URL:', import.meta.env.VITE_WS_URL);
console.log('API URL:', import.meta.env.VITE_API_URL);
```

**Expected:**
```
WS URL: wss://website-ai-2-production.up.railway.app/ws
API URL: https://website.jessicaleetingley.workers.dev
```

**If you see `undefined`:**
- Variables aren't in the build
- Frontend needs to be rebuilt

### Method 2: Check Build Logs

1. Cloudflare Dashboard → Pages → `website-ai-2`
2. Deployments tab
3. Click latest deployment
4. Check build logs

Look for:
- When was it built? (before or after you added variables?)
- Any errors in build?

## Solution: Force Rebuild

### Option 1: Push Empty Commit (Easiest)

```bash
cd lovable-clone
git commit --allow-empty -m "Trigger rebuild with environment variables"
git push
```

This triggers a new build with the variables.

### Option 2: Retry Deployment

1. Cloudflare Dashboard → Pages → `website-ai-2`
2. Deployments tab
3. Click on latest deployment
4. Click "Retry deployment" or "Redeploy"

### Option 3: Make Small Change

Make a tiny change to trigger rebuild:

```bash
cd lovable-clone/frontend
# Touch a file or make tiny change
echo "// rebuild trigger" >> src/App.tsx
git add .
git commit -m "Trigger rebuild"
git push
```

## Verify After Rebuild

1. Wait for deployment to finish
2. Visit your site
3. Check browser console again:

```javascript
console.log('WS URL:', import.meta.env.VITE_WS_URL);
```

Should now show the URL (not undefined).

## Other Possible Issues

If variables ARE in the build but still not working:

1. **Backend not running?**
   ```bash
   curl https://website-ai-2-production.up.railway.app/health
   ```

2. **WebSocket endpoint wrong?**
   - Check URL uses `wss://` (secure)
   - Check endpoint exists: `/ws`

3. **CORS errors?**
   - Check browser console for CORS errors
   - Update backend CORS settings if needed

## Quick Test

Run this in browser console to test WebSocket:

```javascript
const ws = new WebSocket('wss://website-ai-2-production.up.railway.app/ws');
ws.onopen = () => console.log('✅ Connected!');
ws.onerror = (e) => console.error('❌ Error:', e);
```

## Summary

**If variables are set but not working:**
1. ✅ Check if they're actually in the build (browser console test)
2. ✅ If undefined → rebuild frontend (push commit)
3. ✅ If defined but failing → check backend/WebSocket

Try the browser console test first to see if variables are actually in the build!

