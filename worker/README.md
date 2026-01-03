# Cloudflare Worker - Backend Proxy

This Cloudflare Worker proxies HTTP requests to your Python FastAPI backend running on Railway/Render/Fly.io.

## Architecture

```
Frontend (Cloudflare Pages)
    ↓
Cloudflare Worker (Proxy)
    ↓
Python Backend (Railway/Render/Fly.io)
    ↓
Supabase
```

## Setup

### 1. Install Dependencies

```bash
cd worker
npm install
```

### 2. Configure Backend URL

**Option A: Using Wrangler CLI (Recommended)**

```bash
# Set the backend URL as a secret
wrangler secret put BACKEND_URL
# Enter your backend URL when prompted, e.g.: https://your-app.railway.app
```

**Option B: Using Cloudflare Dashboard**

1. Go to Cloudflare Dashboard → Workers & Pages
2. Select your worker
3. Go to Settings → Variables
4. Add variable:
   - Name: `BACKEND_URL`
   - Value: `https://your-backend.railway.app`

### 3. Deploy

```bash
# Deploy to Cloudflare
npm run deploy

# Or using wrangler directly
wrangler deploy
```

### 4. Test

```bash
# Test health endpoint
curl https://website.jessicaleetingley.workers.dev/health

# Should return: {"status":"ok"}
```

## WebSocket Support

**Important:** Cloudflare Workers have limited WebSocket support. For full WebSocket proxying, you have two options:

### Option 1: Direct Connection (Recommended)
Have your frontend connect directly to your backend for WebSocket connections:

```typescript
// In your frontend code
const wsUrl = import.meta.env.VITE_WS_URL || 'wss://your-backend.railway.app/ws';
const ws = new WebSocket(wsUrl);
```

### Option 2: Durable Objects (Advanced)
For full WebSocket proxying through Cloudflare, you'd need to use Durable Objects. This is more complex but provides better WebSocket support.

## Development

```bash
# Run locally
npm run dev

# View logs
npm run tail

# Deploy
npm run deploy
```

## Environment Variables

Set these in Cloudflare Dashboard → Workers → Settings → Variables:

- `BACKEND_URL` (required) - Your Python backend URL
  - Example: `https://your-app.railway.app`

## Routes

The worker will proxy all requests to your backend. For example:

- `https://website.jessicaleetingley.workers.dev/health` → `https://your-backend.railway.app/health`
- `https://website.jessicaleetingley.workers.dev/api/*` → `https://your-backend.railway.app/api/*`

## CORS

The worker automatically adds CORS headers to allow requests from your frontend. Make sure your backend also has CORS configured correctly.

## Troubleshooting

### Backend not responding
- Check that `BACKEND_URL` is set correctly
- Verify your backend is running and accessible
- Check backend logs

### CORS errors
- Ensure backend CORS settings allow your Cloudflare Worker domain
- Check that CORS headers are being forwarded correctly

### WebSocket not working
- Use direct connection to backend for WebSockets (see above)
- Or implement Durable Objects for full WebSocket support

