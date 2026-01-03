# Preview Feature Not Fully Implemented

## Current Status

The WebSocket connection is working and code generation/editing functionality is operational. However, the **preview/iframe feature is not fully implemented** in the migrated version.

## What's Working

✅ WebSocket connection to backend  
✅ Database integration (Supabase)  
✅ Code generation and editing  
✅ Conversation history  
✅ Session management  

## What's Not Working

❌ Live preview of generated code in iframe  
❌ The backend creates code files but doesn't serve them  

## Why This Happens

The original Beam-based system used sandboxes that automatically served the generated React apps. Our migrated version stores code files but doesn't have a mechanism to:

1. Build the React apps (run `npm install` and `npm run build`)
2. Serve the built files via HTTP

## Current Behavior

When you create a session, the backend returns `null` for the URL, so the frontend shows "Connecting to Workspace..." instead of trying to load a 404 page.

## Future Implementation Options

To implement the preview feature, you could:

### Option 1: Serve Built Files via FastAPI
- Add a route to serve static files from the built projects
- Build projects when code changes
- Serve the built `dist/` folder

### Option 2: Use a Code Execution Service
- Integrate with services like:
  - CodeSandbox API
  - StackBlitz SDK
  - Repl.it API
  - Or build your own service

### Option 3: Build and Deploy to Static Hosting
- When code is generated, build and deploy to:
  - Cloudflare Pages (per session)
  - Vercel
  - Netlify
  - Or generate preview URLs

### Option 4: Use iframe srcdoc (Simple but Limited)
- Generate HTML and serve it inline via `srcdoc`
- Limited - won't work for full React apps
- Good for simple HTML/CSS/JS

## For Now

The app works for:
- Chatting with the AI
- Generating code
- Storing code in the database
- Viewing conversation history

But you won't see a live preview until the preview feature is implemented.

## Testing Code Generation

Even without the preview, you can test that code generation works by:

1. Sending a message like "Create a simple todo app"
2. Check the database to see if code files were created
3. The code will be stored in Supabase `code_files` table

The core AI functionality is working - the preview is just a display layer that needs additional implementation.
