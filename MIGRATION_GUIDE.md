# Migration Guide: From Beam to Supabase

This guide explains the changes made to transform the educational lovable-clone into a production-ready system using Supabase and multiple AI models.

## Key Changes

### 1. Backend Infrastructure
- **Before**: Beam Cloud with Sandboxes for code execution
- **After**: Supabase for data storage + Local file system for code execution

### 2. AI Models
- **Before**: Single OpenAI model (o4-mini)
- **After**: Multiple models:
  - Claude 3.5 Sonnet (Planning/High-reasoning)
  - GPT-4o (Vision/Quick edits)
  - GPT-4o-mini (Fast coding - Gemini equivalent coming)

### 3. Server Architecture
- **Before**: Beam realtime decorator
- **After**: FastAPI with WebSocket support

### 4. Data Storage
- **Before**: In-memory session data
- **After**: Supabase PostgreSQL with tables:
  - `sessions`: User sessions and project metadata
  - `code_files`: Code file storage
  - `conversations`: Conversation history

## Setup Instructions

### 1. Supabase Setup

1. Create a Supabase project at https://supabase.com
2. Run the SQL schema from `supabase_schema.sql` in your Supabase SQL Editor
3. Get your Supabase URL and keys from Project Settings > API

### 2. Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
# API Keys
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-key
SUPABASE_SERVICE_ROLE_KEY=your-key
```

### 3. Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Generate BAML Clients

After updating BAML files:

```bash
make generate
# or
baml-cli generate
```

### 5. Run the Server

```bash
python -m src.server
# or
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

### 6. Update Frontend

Update the frontend WebSocket URL to point to your new server:

```env
VITE_WS_URL=ws://localhost:8000/ws
```

## Architecture Differences

### Code Execution
- Beam used isolated sandboxes with Docker
- New system uses local file system (can be enhanced with Docker later)
- Projects stored in `./projects/{session_id}/`

### Session Management
- Beam: In-memory dictionary
- Supabase: Persistent database with RLS policies

### API Models
- The new system supports multiple AI models via BAML
- Planning uses Claude (high-reasoning)
- Quick edits use GPT-4o-mini (fast, low-latency)

## Next Steps for Production

1. **Code Execution**: Consider Docker containers or a dedicated execution service
2. **Authentication**: Implement proper user authentication with Supabase Auth
3. **RLS Policies**: Update Row Level Security policies for multi-user support
4. **Deployment**: Deploy FastAPI server (e.g., on Railway, Render, or AWS)
5. **Gemini Integration**: Add Gemini 2.5 Flash when BAML supports it
6. **Monitoring**: Add logging and monitoring (e.g., Sentry, Datadog)

## File Structure

```
src/
  ├── agent_v2.py       # New agent with Supabase integration
  ├── server.py         # FastAPI server
  ├── database.py       # Supabase database interface
  ├── code_executor.py  # File system code execution
  ├── config.py         # Configuration management
  ├── agent.py          # Old Beam-based agent (kept for reference)
  └── tools.py          # Old Beam tools (kept for reference)
```

## Migration Checklist

- [x] Add Supabase dependencies
- [x] Create database schema
- [x] Update BAML for multiple AI models
- [x] Create new agent with Supabase
- [x] Create FastAPI server
- [x] Create code executor
- [ ] Update frontend WebSocket URL
- [ ] Test end-to-end workflow
- [ ] Deploy to production

