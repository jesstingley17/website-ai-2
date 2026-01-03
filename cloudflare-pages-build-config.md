# Cloudflare Pages Build Configuration

Use these settings when setting up your project in Cloudflare Pages:

## Build Configuration

- **Framework preset**: `Vite` (or "None")
- **Build command**: 
  ```bash
  cd frontend && npm install && npm run build
  ```
- **Build output directory**: 
  ```
  frontend/dist
  ```
- **Root directory**: 
  ```
  (leave empty or `/`)
  ```

## Environment Variables

Add these in Cloudflare Pages → Settings → Environment Variables:

- **Production**:
  ```
  VITE_WS_URL=wss://your-backend-url.railway.app/ws
  ```

- **Preview** (optional, for branch previews):
  ```
  VITE_WS_URL=wss://your-backend-url.railway.app/ws
  ```

Replace `your-backend-url.railway.app` with your actual backend deployment URL.

## Notes

- Make sure your backend is deployed and running before setting `VITE_WS_URL`
- The backend URL should use `wss://` (secure WebSocket) for HTTPS sites
- Cloudflare Pages will automatically rebuild on git push to `main`

