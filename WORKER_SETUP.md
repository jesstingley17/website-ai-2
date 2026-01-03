# Cloudflare Worker Proxy - Quick Setup

## What This Does

The Worker at `website.jessicaleetingley.workers.dev` will proxy HTTP requests to your Python backend, giving you:
- ✅ Edge network benefits
- ✅ CORS handling
- ✅ Request forwarding
- ⚠️ Limited WebSocket support (see below)

## Quick Start

### Step 1: Install Dependencies

```bash
cd worker
npm install
```

### Step 2: Set Backend URL

You need to tell the Worker where your Python backend is running.

**Option A: Using Wrangler CLI**

```bash
# Make sure you're logged in
wrangler login

# Set the backend URL
wrangler secret put BACKEND_URL
# When prompted, enter: https://your-backend.railway.app
# (Replace with your actual backend URL)
```

**Option B: Using Cloudflare Dashboard**

1. Go to https://dash.cloudflare.com
2. Workers & Pages → Your Worker (`website`)
3. Settings → Variables
4. Add variable:
   - Name: `BACKEND_URL`
   - Value: `https://your-backend.railway.app`

### Step 3: Deploy

```bash
cd worker
npm run deploy
```

Or:
```bash
wrangler deploy
```

### Step 4: Test

```bash
# Test the proxy
curl https://website.jessicaleetingley.workers.dev/health

# Should return: {"status":"ok"}
```

## Architecture

```
┌─────────────────────────┐
│  Cloudflare Pages       │
│  (Frontend)             │
└───────────┬─────────────┘
            │
            ↓ HTTP
┌─────────────────────────┐
│  Cloudflare Worker      │
│  (Proxy)                │
│  website.*.workers.dev  │
└───────────┬─────────────┘
            │
            ↓ HTTP
┌─────────────────────────┐
│  Python Backend         │
│  (Railway/Render/etc.)  │
└───────────┬─────────────┘
            │
            ↓
┌─────────────────────────┐
│  Supabase               │
└─────────────────────────┘
```

## WebSocket Handling

**Important:** Cloudflare Workers have limited WebSocket proxying capabilities. For WebSocket connections, you have two options:

### Option 1: Direct Connection (Recommended)

Have your frontend connect directly to your backend for WebSockets:

```typescript
// In frontend/src/config/beam.ts or similar
export const BEAM_CONFIG = {
  WS_URL: import.meta.env.VITE_WS_URL || 'wss://your-backend.railway.app/ws',
  // Use Worker for HTTP, direct for WebSocket
  API_URL: 'https://website.jessicaleetingley.workers.dev',
} as const;
```

### Option 2: Update Frontend to Use Worker for HTTP

Update your frontend to use the Worker URL for HTTP requests:

```typescript
// Use Worker for API calls
const API_URL = 'https://website.jessicaleetingley.workers.dev';

// Use direct backend for WebSockets
const WS_URL = 'wss://your-backend.railway.app/ws';
```

## Update Your Frontend

After deploying the Worker, update your frontend environment variables in Cloudflare Pages:

1. Go to Cloudflare Pages → Your Project → Settings → Environment Variables
2. Add/Update:
   ```
   VITE_API_URL=https://website.jessicaleetingley.workers.dev
   VITE_WS_URL=wss://your-backend.railway.app/ws
   ```

## Next Steps

1. ✅ Deploy Python backend to Railway/Render/Fly.io
2. ✅ Set `BACKEND_URL` in Worker
3. ✅ Deploy Worker
4. ✅ Update frontend environment variables
5. ✅ Test the connection

## Troubleshooting

### Worker returns 500 "BACKEND_URL not configured"
- Set the `BACKEND_URL` secret/variable (see Step 2)

### Worker returns 502 "Backend unavailable"
- Check that your backend is running
- Verify the `BACKEND_URL` is correct
- Check backend logs

### CORS errors
- The Worker adds CORS headers automatically
- Also ensure your backend CORS allows the Worker domain

### WebSocket not working
- Use direct connection to backend for WebSockets (see above)
- Workers have limited WebSocket support

## Files Created

- `worker/src/index.ts` - Worker code
- `worker/wrangler.toml` - Worker configuration
- `worker/package.json` - Dependencies
- `worker/tsconfig.json` - TypeScript config
- `worker/README.md` - Detailed documentation

