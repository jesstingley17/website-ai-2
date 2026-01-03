# Deploy Frontend to Cloudflare Pages via CLI

## ✅ Build Complete!

Your frontend has been built successfully. The files are in `frontend/dist/`.

## Authentication Options

### Option 1: Interactive Login (Easiest)

Run this command in your terminal (it will open a browser):

```bash
cd frontend
wrangler login
```

Then deploy:

```bash
wrangler pages deploy dist --project-name=your-project-name
```

### Option 2: API Token (For CI/CD)

1. Get API token: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/
2. Set it:
   ```bash
   export CLOUDFLARE_API_TOKEN=your-token-here
   ```
3. Deploy:
   ```bash
   wrangler pages deploy dist --project-name=your-project-name
   ```

## Project Name

Replace `your-project-name` with your actual Cloudflare Pages project name.

**If you don't have a project yet:**
- You can create it via dashboard first
- OR wrangler will create it if the name doesn't exist

**Common names:**
- `website-ai-2`
- `lovable-clone`
- `your-chosen-name`

## Full Deploy Command

```bash
cd frontend
wrangler login  # First time only
wrangler pages deploy dist --project-name=your-project-name
```

## Alternative: Use Dashboard

If CLI is too complex, you can:
1. Go to Cloudflare Dashboard → Pages
2. Create/select your project
3. Upload the `dist` folder manually
4. Or connect GitHub and let it auto-deploy

## Next Steps After Deploy

Once deployed:
1. Get your Pages URL (e.g., `https://your-project.pages.dev`)
2. Set environment variables in Pages dashboard
3. Test your frontend!

