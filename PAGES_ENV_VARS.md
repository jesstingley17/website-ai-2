# Cloudflare Pages Environment Variables

## Do You Need Them?

**Yes, but set them AFTER the first successful deployment.**

## Required Variables

After your frontend deploys successfully, add these in Cloudflare Pages → Settings → Environment Variables:

### For Production:

```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

### For Preview (optional):

```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

## What Each Variable Does

- **`VITE_WS_URL`**: WebSocket URL for real-time communication
  - Points directly to your Railway backend
  - Uses `wss://` (secure WebSocket)

- **`VITE_API_URL`**: API URL for HTTP requests
  - Points to your Cloudflare Worker (which proxies to Railway)
  - Or you could point directly to Railway: `https://website-ai-2-production.up.railway.app`

## When to Set Them

1. **First**: Deploy without variables (just to get it working)
2. **Then**: Add environment variables
3. **Finally**: Redeploy (or push a commit to trigger rebuild)

## How to Set Them

1. Go to Cloudflare Dashboard → Pages → Your Project
2. Settings → Environment Variables
3. Add variables for **Production** and **Preview** (if needed)
4. Save
5. Pages will automatically rebuild with new variables

## Alternative: Direct to Railway

If you want to skip the Worker proxy, you can point directly to Railway:

```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website-ai-2-production.up.railway.app
```

But using the Worker proxy is recommended for edge benefits.

## Summary

- ✅ **Set them AFTER first deployment**
- ✅ **Required for frontend to connect to backend**
- ✅ **Pages will rebuild automatically when you add them**

