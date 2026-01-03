# Quick Help Guide

## 🆘 What Do You Need Help With?

### 1. Setting Up the Preview Feature (Just Added!)

The preview feature needs `BACKEND_URL` to be set in Railway:

**In Railway Dashboard:**
1. Go to your project → **Variables**
2. Add new variable:
   - **Name**: `BACKEND_URL`
   - **Value**: `https://website-ai-2-production.up.railway.app`
3. Save (Railway will redeploy automatically)

**Test it:**
- Visit: `https://website-ai-2-production.up.railway.app/preview/test-session`
- Should show a preview page (even if empty)

### 2. Testing Your Setup

**Quick Checklist:**

✅ **Backend Health Check:**
```
https://website-ai-2-production.up.railway.app/health
```
Should return: `{"status":"ok"}`

✅ **Frontend:**
- Visit your Cloudflare Pages URL
- Open browser console (F12)
- Check for errors
- Try creating a session

✅ **Database:**
- Supabase tables created? (sessions, code_files, conversations)
- Environment variables set in Railway?

✅ **Environment Variables:**
- Railway: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `BACKEND_URL`
- Cloudflare Pages: `VITE_WS_URL`, `VITE_API_URL`

### 3. Common Issues

**Issue: "Connecting to Workspace..." forever**
- Check browser console for errors
- Verify `VITE_WS_URL` is set in Cloudflare Pages
- Check Railway logs for backend errors

**Issue: Database errors**
- Run the SQL schema in Supabase (supabase_schema.sql)
- Verify Supabase environment variables are set

**Issue: Preview shows 404**
- Set `BACKEND_URL` in Railway (see #1 above)
- Check Railway logs

**Issue: Code generation not working**
- Check OpenAI/Anthropic API keys are set
- Check Railway logs for API errors
- Verify database tables exist

### 4. What's Currently Working

✅ WebSocket connection to backend  
✅ Database integration (Supabase)  
✅ Code generation and editing  
✅ Session management  
✅ Chat functionality  
✅ Simple preview (basic React components)  

### 5. What's Not Fully Working

⚠️ Preview is limited:
- Only works for simple React components
- No imports, no npm packages
- Single file (App.tsx) only
- Not like full lovable.dev yet

### 6. Next Steps You Can Take

**Option A: Use Current Setup (Good for Learning)**
- Test code generation
- Create simple React components
- Learn the system
- Build from here

**Option B: Enhance Preview**
- Add support for more features
- Improve error handling
- Add more React hooks support

**Option C: Full Implementation**
- Integrate CodeSandbox API
- Or build custom build system
- Much more complex but full-featured

### 7. Getting More Help

**Check These Files:**
- `PREVIEW_IMPLEMENTATION.md` - Preview details
- `FINAL_SETUP.md` - Setup steps
- `WEBSOCKET_CONNECTION_FIX.md` - Connection issues
- `SUPABASE_SETUP_DATABASE.md` - Database setup

**What to Share When Asking for Help:**
1. What you're trying to do
2. What error you're seeing (if any)
3. Browser console errors (F12)
4. Railway logs
5. What step you're on

## 🚀 Quick Start Commands

**Test Backend:**
```bash
curl https://website-ai-2-production.up.railway.app/health
```

**Check Railway Logs:**
- Railway Dashboard → Your service → Logs

**Check Frontend Console:**
- Open your site → F12 → Console tab

**Check Environment Variables:**
- Railway: Dashboard → Variables
- Cloudflare Pages: Dashboard → Pages → Settings → Environment Variables

## 📝 Current Status Summary

**Working:**
- ✅ Backend server running
- ✅ Database connected
- ✅ WebSocket connection
- ✅ Code generation
- ✅ Basic preview

**Needs Setup:**
- ⚙️ BACKEND_URL in Railway (for preview)
- ⚙️ Environment variables verified

**Future Work:**
- 🔮 Full preview system (like lovable.dev)
- 🔮 Multiple file support
- 🔮 npm packages support
- 🔮 Build system integration
