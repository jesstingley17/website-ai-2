# Troubleshooting "Site Doesn't Look Right"

## What You're Seeing

"Connecting to Workspace..." means you're on the `/create` route, which is the workspace/editor screen.

## What You Should See

The home page (route `/`) should show:
- Title: "What do you want build?"
- Subtitle: "Build a website with Beam Sandboxes."
- A textarea input: "What do you want to build?"
- A "Start Building" button

## Quick Fixes

### Fix 1: Go to Home Page

Make sure you're visiting:
```
https://website-ai-2.pages.dev/
```

NOT:
```
https://website-ai-2.pages.dev/create
```

The home page is `/` (root), not `/create`.

### Fix 2: Check Browser Console

1. Open DevTools (F12)
2. Go to Console tab
3. Look for errors (red text)

Common issues:
- CSS not loading
- JavaScript errors
- Missing assets

### Fix 3: Clear Cache

Sometimes cached files cause issues:
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Or clear browser cache
3. Or use incognito/private mode

## What Should Happen

1. **Home Page** (`/`):
   - Shows "What do you want build?" form
   - You enter what you want to build
   - Click "Start Building"

2. **Create Page** (`/create?session_id=...`):
   - Shows workspace with preview
   - This is where "Connecting to Workspace..." appears
   - Needs WebSocket connection to backend

## Check These

1. **What URL are you on?**
   - Home: `https://website-ai-2.pages.dev/`
   - Create: `https://website-ai-2.pages.dev/create?...`

2. **What do you see?**
   - Home page form? ✅
   - "Connecting to Workspace..."? (means you're on /create)
   - Blank page? (check console)
   - Broken styling? (CSS not loading)

3. **Browser console errors?**
   - Open F12 → Console
   - Share any red errors

## Next Steps

1. Visit the home page: `https://website-ai-2.pages.dev/`
2. Check what you see
3. Open browser console (F12)
4. Share what looks wrong or any errors

This will help identify the specific issue!

