# Railway Environment Variables - Quick Checklist

## Required Variables (Must Set)

These are **required** - your server won't start without them:

### 1. API Keys
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Supabase (Database)
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Server Config
```
HOST=0.0.0.0
```

**Note:** Railway automatically sets `PORT` - don't set it manually!

## Optional Variables (Can Skip for Now)

```
GOOGLE_API_KEY=... (only if using Gemini)
DEBUG=false
PROJECTS_DIR=./projects
```

## How to Set Variables in Railway

1. In Railway dashboard, click on your project
2. Go to **"Variables"** tab (or click on your service → Variables)
3. Click **"New Variable"**
4. Add each variable:
   - **Name**: e.g., `OPENAI_API_KEY`
   - **Value**: Your actual key
   - Click **"Add"**
5. Repeat for all variables

## Where to Get Your Keys

### OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create new key
- Copy it (starts with `sk-`)

### Anthropic API Key
- Go to https://console.anthropic.com/settings/keys
- Create new key
- Copy it (starts with `sk-ant-`)

### Supabase Keys
- Go to your Supabase project dashboard
- Settings → API
- Copy:
  - **Project URL** → `SUPABASE_URL`
  - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY`

## Quick Copy-Paste List

Copy these and fill in the values:

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
HOST=0.0.0.0
```

## After Setting Variables

1. Railway will automatically redeploy
2. Check the logs - you should see "Agent initialized"
3. Test: `https://your-app.railway.app/health`

## Troubleshooting

**Server fails to start:**
- Check all required variables are set
- Verify variable names are exact (case-sensitive)
- Check values don't have extra spaces

**"Configuration errors" in logs:**
- Missing required variable
- Check which variable is missing in error message

**Database connection fails:**
- Verify `SUPABASE_URL` is correct
- Verify `SUPABASE_SERVICE_ROLE_KEY` is the service_role key (not anon key)

