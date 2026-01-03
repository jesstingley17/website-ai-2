# Quick Reference: Cloudflare Pages Settings

## When Setting Up in Cloudflare Dashboard

### Build Configuration:
```
Build command: cd frontend && npm install && npm run build
Build output directory: frontend/dist
Root directory: (leave empty)
Framework preset: Vite (or None)
```

### Environment Variables:
```
VITE_WS_URL=wss://your-backend.railway.app/ws
```
(Add this after you deploy your backend!)

---

**Important**: You'll need to deploy your Python backend separately (Railway, Render, Fly.io, etc.) since Cloudflare Workers don't support Python/FastAPI.

See `CLOUDFLARE_DEPLOYMENT.md` for full instructions.

