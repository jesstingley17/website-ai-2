# Cloudflare Pages Form Submission Error - Troubleshooting

## The Error

"An internal error prevented the form from submitting. Please try again."

## Common Causes & Solutions

### 1. Browser/Network Issues

**Try:**
- Refresh the page (F5)
- Clear browser cache
- Try a different browser (Chrome, Firefox, Safari)
- Try incognito/private mode
- Check your internet connection

### 2. Cloudflare Dashboard Issue

**Try:**
- Log out and log back in
- Wait a few minutes and try again
- Check Cloudflare status page for outages

### 3. Invalid Configuration

**Check your settings:**
- Build command: `cd frontend && npm install && npm run build`
- Output directory: `frontend/dist`
- Deploy command: `echo "Built"` (keep it simple)

**Common issues:**
- Special characters in commands
- Very long commands
- Invalid paths

### 4. Session Timeout

**Solution:**
- Log out and log back in
- Try the form again

### 5. Field Validation Issues

**Make sure:**
- Build command doesn't have syntax errors
- Output directory path is correct (no leading slash usually)
- All required fields are filled

## Alternative: Use Wrangler CLI

If the dashboard keeps failing, you can configure via CLI:

```bash
cd frontend
npm install
npm run build

# Deploy to Pages
wrangler pages deploy dist --project-name=your-project-name
```

## Quick Fix Steps

1. **Refresh the page**
2. **Check your settings are valid**
3. **Try a simpler deploy command**: `echo "ok"`
4. **Try a different browser**
5. **Wait 5 minutes and try again**

## If Nothing Works

You can also:
- Delete and recreate the Pages project
- Use Wrangler CLI to deploy instead
- Contact Cloudflare support

Let me know what happens when you try these steps!

