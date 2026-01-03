# Cloudflare Pages Configuration Settings

## Correct Settings for Your Project

### Framework preset
**Vite** (or "None" if Vite isn't listed)

### Build command
```
cd frontend && npm install && npm run build
```

### Build output directory
```
frontend/dist
```

### Root directory (advanced)
Leave **empty** (or set to `/` if you get errors)

### Deploy command (if shown/required)
```
echo "Frontend built successfully"
```
OR leave empty if the field is optional

### Environment variables (after deployment)
You'll add these after the first deployment:
- `VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws`
- `VITE_API_URL=https://website.jessicaleetingley.workers.dev`

## Why These Settings?

- **Build command**: Installs dependencies and builds your React/Vite app
- **Output directory**: Points to where Vite puts the built files (`frontend/dist`)
- **Root directory**: Empty because your repo root contains both frontend and backend
- **Deploy command**: No-op because Pages just serves static files (no server needed)

## Important Notes

❌ **Don't set deploy command to**: `python -m src.server`
✅ **Do set deploy command to**: `echo "ok"` (or leave empty)

Your Python backend runs on Railway, not Cloudflare Pages!

## After Saving

1. Cloudflare will build your frontend
2. You'll get a URL like `https://your-project.pages.dev`
3. Then add environment variables
4. Update Worker BACKEND_URL if needed
5. Test everything!

