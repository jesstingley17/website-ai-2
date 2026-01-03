# Port Configuration - Railway

## How Railway Ports Work

Railway:
- ✅ **Automatically sets** `PORT` environment variable
- ✅ **Maps it internally** to the public URL
- ✅ **Public URL has no port** (just `https://domain.railway.app`)

Your application:
- ✅ Should use `os.getenv("PORT")` 
- ✅ Railway sets PORT automatically (could be any port like 8888, 3000, etc.)
- ✅ You don't need to set PORT manually

## Your Current Code

Looking at `src/config.py`:
```python
PORT = int(os.getenv("PORT", "8000"))
```

This is **correct** - it reads PORT from environment (which Railway sets).

## The Real Issue (502 Error)

The 502 error means your **application isn't starting**, not a port problem.

Common causes:
1. **Missing environment variables** (most likely)
2. **Application crashes on startup**
3. **Configuration errors**

## What to Check

### 1. Check Railway Logs

Go to Railway → Your Service → Deployments → Latest → View Logs

Look for:
- ✅ Good: `Uvicorn running on http://0.0.0.0:PORT`
- ❌ Bad: `Configuration errors: ...`
- ❌ Bad: `ValueError: ...`
- ❌ Bad: Any red error messages

### 2. Verify Environment Variables

In Railway → Variables, make sure you have:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `HOST=0.0.0.0`

**Don't set PORT** - Railway sets it automatically!

### 3. Check Start Command

In Railway → Settings → Service:
- **Start Command**: `python -m src.server`
- **Root Directory**: `lovable-clone`

## About Port 8888

If Railway is using port 8888 internally, that's fine! Your code should automatically use it via `os.getenv("PORT")`. The public URL doesn't show the port - it's just:
```
https://website-ai-2-production.up.railway.app
```

## Next Steps

1. **Check Railway logs** - This will show the actual error
2. **Verify all env vars are set**
3. **Check start command is correct**

The port configuration should be fine - the issue is likely missing environment variables or a startup error. Check the logs!

