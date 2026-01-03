# Wrangler Pages Deploy Command

## Important Distinction

- `wrangler deploy` - Deploys **Workers** (JavaScript/TypeScript)
- `wrangler pages deploy` - Deploys **Pages** (static sites)

Since you're deploying a static frontend, you need **`wrangler pages deploy`**.

## Correct Command for Your Frontend

```bash
cd frontend
wrangler pages deploy dist --project-name=your-project-name
```

## Full Steps

### 1. Authenticate (First Time Only)

```bash
wrangler login
```

This opens your browser to authenticate with Cloudflare.

### 2. Deploy

```bash
cd frontend
wrangler pages deploy dist --project-name=your-project-name
```

Replace `your-project-name` with your actual Cloudflare Pages project name.

## Command Reference

Based on [Cloudflare Wrangler documentation](https://developers.cloudflare.com/workers/wrangler/commands/):

### `wrangler pages deploy`

Deploys a directory to Cloudflare Pages.

**Syntax:**
```bash
wrangler pages deploy <DIRECTORY> [OPTIONS]
```

**Options:**
- `--project-name` or `-p` - Name of your Pages project
- `--branch` - Git branch name (optional)
- `--commit-hash` - Git commit hash (optional)
- `--commit-message` - Git commit message (optional)
- `--commit-dirty` - Whether the working directory is dirty (optional)

**Example:**
```bash
wrangler pages deploy dist --project-name=my-site
```

## Your Specific Case

Since you've already built the frontend:

```bash
# You're in the frontend directory, dist/ folder exists
wrangler pages deploy dist --project-name=your-project-name
```

## Finding Your Project Name

If you don't know your project name:
1. Check Cloudflare Dashboard → Pages
2. Look for your project name
3. Or create a new one - wrangler can create it if it doesn't exist

## Authentication Issues

If you get authentication errors:
```bash
wrangler login
```

Or set an API token:
```bash
export CLOUDFLARE_API_TOKEN=your-token-here
```

Get tokens from: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/

## After Deployment

Once deployed, you'll get a URL like:
- `https://your-project-name.pages.dev`

Then you can:
1. Set environment variables in the dashboard
2. Update Worker `BACKEND_URL` to point to your Railway backend
3. Test everything!

