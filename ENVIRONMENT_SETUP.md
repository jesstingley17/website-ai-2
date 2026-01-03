# Environment Variables Setup Guide

## Required API Keys & Environment Variables

### 🔑 **Required API Keys**

#### 1. **OpenAI API Key** (REQUIRED)
- **Variable**: `OPENAI_API_KEY`
- **Where to get it**: https://platform.openai.com/api-keys
- **Used for**: GPT-4o and GPT-4o-mini models (code editing)
- **Cost**: Pay-per-use (check OpenAI pricing)

#### 2. **Anthropic API Key** (REQUIRED)
- **Variable**: `ANTHROPIC_API_KEY`
- **Where to get it**: https://console.anthropic.com/settings/keys
- **Used for**: Claude 3.5 Sonnet (planning/high-reasoning)
- **Cost**: Pay-per-use (check Anthropic pricing)

#### 3. **Supabase Configuration** (REQUIRED)
- **Variable**: `SUPABASE_URL`
  - Get from: Supabase Dashboard > Project Settings > API > Project URL
  - Format: `https://xxxxx.supabase.co`
  
- **Variable**: `SUPABASE_ANON_KEY` (REQUIRED)
  - Get from: Supabase Dashboard > Project Settings > API > Project API keys > anon/public
  - Used for: Client-side database access
  
- **Variable**: `SUPABASE_SERVICE_ROLE_KEY` (OPTIONAL but recommended)
  - Get from: Supabase Dashboard > Project Settings > API > Project API keys > service_role
  - Used for: Server-side database operations (bypasses RLS)
  - ⚠️ **Keep this secret!** Never expose in frontend code

### 📋 **Optional Variables**

#### 4. **Google API Key** (OPTIONAL - Future Gemini support)
- **Variable**: `GOOGLE_API_KEY`
- **Where to get it**: https://makersuite.google.com/app/apikey
- **Used for**: Gemini 2.5 Flash (when BAML supports it)
- **Status**: Currently not used, reserved for future

### ⚙️ **Server Configuration** (Optional - has defaults)

- **Variable**: `HOST`
  - Default: `0.0.0.0`
  - The host to bind the server to

- **Variable**: `PORT`
  - Default: `8000`
  - The port to run the server on

- **Variable**: `DEBUG`
  - Default: `false`
  - Set to `true` for development debugging

- **Variable**: `PROJECTS_DIR`
  - Default: `./projects`
  - Directory where code projects are stored

## 📝 Complete .env File Template

Create a `.env` file in the `lovable-clone` directory:

```bash
# === REQUIRED API KEYS ===

# OpenAI (for GPT-4o and GPT-4o-mini)
OPENAI_API_KEY=sk-...

# Anthropic (for Claude 3.5 Sonnet)
ANTHROPIC_API_KEY=sk-ant-...

# === REQUIRED SUPABASE CONFIGURATION ===

# Supabase Project URL
SUPABASE_URL=https://xxxxx.supabase.co

# Supabase Anon Key (public, safe for client-side)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Supabase Service Role Key (secret, server-side only!)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# === OPTIONAL: Google (for future Gemini support) ===
# GOOGLE_API_KEY=your-google-api-key

# === OPTIONAL: Server Configuration ===
# HOST=0.0.0.0
# PORT=8000
# DEBUG=false
# PROJECTS_DIR=./projects
```

## 🚀 Quick Setup Steps

### 1. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. ⚠️ Save it immediately - you can't view it again!

### 2. Get Anthropic API Key
1. Go to https://console.anthropic.com/settings/keys
2. Sign in or create account
3. Click "Create Key"
4. Copy the key (starts with `sk-ant-`)
5. ⚠️ Save it immediately - you can't view it again!

### 3. Set Up Supabase
1. Go to https://supabase.com
2. Create a free account
3. Click "New Project"
4. Fill in project details:
   - Name: `lovable-clone` (or any name)
   - Database Password: (choose a strong password - save it!)
   - Region: (choose closest to you)
5. Wait for project to initialize (~2 minutes)
6. Go to **Project Settings > API**
7. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon/public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY` (keep secret!)
8. Go to **SQL Editor**
9. Create a new query
10. Paste the contents of `supabase_schema.sql`
11. Click "Run" to create the database tables

### 4. Create .env File

```bash
cd lovable-clone
cp .env.example .env  # If .env.example exists
# Or create .env manually with the template above
```

Edit `.env` and fill in all your keys.

### 5. Test Configuration

```bash
# Activate virtual environment
source venv/bin/activate

# The server will validate on startup
python -m src.server
```

If you see "Configuration errors", check which variables are missing.

## 🔒 Security Best Practices

1. **Never commit `.env` to git** - It's already in `.gitignore`
2. **Use Service Role Key carefully** - Only in server-side code
3. **Rotate keys regularly** - Especially if exposed
4. **Use environment variables in production** - Don't hardcode keys
5. **Limit API key permissions** - Use least privilege principle

## 💰 Cost Estimates

- **OpenAI GPT-4o**: ~$0.005 per 1K input tokens, $0.015 per 1K output tokens
- **OpenAI GPT-4o-mini**: ~$0.15 per 1M input tokens, $0.60 per 1M output tokens
- **Anthropic Claude 3.5 Sonnet**: ~$3 per 1M input tokens, $15 per 1M output tokens
- **Supabase**: Free tier includes 500MB database, 2GB bandwidth (sufficient for testing)

For development/testing, expect ~$5-20/month depending on usage.

## ✅ Validation

The application will validate required keys on startup. If any are missing, you'll see an error like:

```
ValueError: Configuration errors: OPENAI_API_KEY is required, SUPABASE_URL is required
```

Fix the missing variables and restart the server.

