# Environment Variable Types - Text vs Secrets

## For Your Frontend Variables

**Set as TEXT (Plain Variables):**

```
VITE_WS_URL=wss://website-ai-2-production.up.railway.app/ws
VITE_API_URL=https://website.jessicaleetingley.workers.dev
```

## Why Text, Not Secrets?

### VITE_ Variables Are Public

Variables starting with `VITE_` are:
- ✅ Embedded into your frontend JavaScript bundle
- ✅ Visible to anyone who views your website's source code
- ✅ Public by design (they're meant to be client-side config)
- ❌ NOT secrets - they can't be hidden

### These Are Public URLs

- `VITE_WS_URL` - Your backend WebSocket URL (public endpoint)
- `VITE_API_URL` - Your API/Worker URL (public endpoint)

These URLs are meant to be public - your frontend needs to know where to connect!

## When to Use Secrets

Use **Secrets** for:
- API keys (like `OPENAI_API_KEY`)
- Database passwords
- Private tokens
- Service account keys

**NOT** for:
- Public URLs
- Frontend configuration
- VITE_ prefixed variables

## In Cloudflare Pages

When adding environment variables:
1. Click "Add variable"
2. Choose **"Text"** (not "Secret")
3. Enter the variable name and value
4. Save

## Summary

- ✅ **Text/Plain**: `VITE_WS_URL`, `VITE_API_URL` (public URLs)
- ❌ **Secrets**: API keys, passwords, tokens (private data)

Your frontend variables are public configuration, so use **Text**!

