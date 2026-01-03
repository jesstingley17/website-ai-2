# Setting Up Supabase Database Schema

The error `Could not find the table 'public.sessions'` means the database tables haven't been created yet. Follow these steps:

## Step 1: Open Supabase SQL Editor

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Click on **SQL Editor** in the left sidebar
4. Click **New Query**

## Step 2: Run the Schema SQL

1. Open the file `supabase_schema.sql` in this repository
2. Copy **ALL** the SQL code from that file
3. Paste it into the Supabase SQL Editor
4. Click **Run** (or press `Ctrl+Enter` / `Cmd+Enter`)

The schema will create:
- `sessions` table - stores user sessions
- `code_files` table - stores code files for each session
- `conversations` table - stores conversation history
- Indexes for performance
- Row Level Security (RLS) policies
- Triggers for auto-updating timestamps

## Step 3: Verify Tables Were Created

1. In Supabase Dashboard, go to **Table Editor**
2. You should see three tables:
   - `sessions`
   - `code_files`
   - `conversations`

## Step 4: Test Your Backend Again

After running the schema, try connecting to your app again. The error should be resolved.

## Quick Copy-Paste SQL

If you can't find the file, here's the SQL to run:

```sql
-- Sessions table to store user sessions and project metadata
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT UNIQUE NOT NULL,
    project_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Code files table to store project code
CREATE TABLE IF NOT EXISTS code_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
    file_path TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(session_id, file_path)
);

-- Conversation history table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_code_files_session_id ON code_files(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);

-- Enable Row Level Security (RLS)
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE code_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth requirements)
-- For now, allow all operations - you should customize these
CREATE POLICY "Allow all operations on sessions" ON sessions
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on code_files" ON code_files
    FOR ALL USING (true) WITH CHECK (true);

CREATE POLICY "Allow all operations on conversations" ON conversations
    FOR ALL USING (true) WITH CHECK (true);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to auto-update updated_at
CREATE TRIGGER update_sessions_updated_at BEFORE UPDATE ON sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_code_files_updated_at BEFORE UPDATE ON code_files
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Troubleshooting

### Error: "relation already exists"
- This means the tables already exist. That's fine - the `IF NOT EXISTS` clauses will skip them.

### Error: "permission denied"
- Make sure you're running this as the project owner
- Check that you have the correct database permissions

### Error: "function already exists"
- The function already exists. This is fine - `CREATE OR REPLACE` will update it.

After running this SQL, your backend should be able to connect to the database successfully!
