# Full Build System Implementation Plan

## Goal
Create a fully functional preview system like lovable.dev that supports:
- Multiple files with imports
- npm packages
- TypeScript
- Full build process (npm install + vite build)
- Real development server or built file serving

## Architecture Options

### Option 1: Build Service (Recommended for Railway)
- Run `npm install` when code changes
- Run `vite build` to create production bundle
- Serve built `dist/` folder via FastAPI
- Pros: Works with Railway, full control
- Cons: Requires process management, slower builds

### Option 2: CodeSandbox API Integration
- Use CodeSandbox's API to create sandboxes
- CodeSandbox handles building and serving
- Pros: Easy integration, battle-tested
- Cons: External dependency, API limits, cost

### Option 3: StackBlitz SDK Integration
- Use StackBlitz WebContainer API
- Runs in browser, no backend needed
- Pros: Modern, runs in browser
- Cons: Browser-only, different architecture

## Recommended: Option 1 - Build Service

### Implementation Steps

1. **Build Service Module**
   - Queue build requests
   - Run `npm install` when dependencies change
   - Run `vite build` when code changes
   - Store build outputs
   - Handle build errors

2. **File Serving**
   - Serve built `dist/` folder via FastAPI
   - Handle routing for SPA
   - Serve static assets

3. **Background Processing**
   - Use asyncio or background tasks
   - Process build queue
   - Cache builds

4. **Build Management**
   - Track build status
   - Handle concurrent builds
   - Clean up old builds

### File Structure
```
src/
  build_service.py    # Build queue and processing
  file_server.py      # Serve built files
  code_executor.py    # Enhanced with build support
  server.py           # Updated endpoints
```

### Endpoints Needed
- `POST /api/build/{session_id}` - Trigger build
- `GET /api/build/{session_id}/status` - Build status
- `GET /preview/{session_id}/*` - Serve built files
- `GET /preview/{session_id}/` - Serve index.html (SPA routing)

## Implementation Phases

### Phase 1: Basic Build System ✅ (We'll start here)
- Run npm install
- Run vite build
- Serve built files
- Basic error handling

### Phase 2: Optimization
- Build caching
- Incremental builds
- Build queue management
- Background processing

### Phase 3: Advanced Features
- Hot reloading
- Build status updates via WebSocket
- Multiple build environments
- Build logs

## Current Status

We have:
- ✅ Code generation working
- ✅ File storage (database + file system)
- ✅ Simple preview (React CDN)
- ❌ Build system (need to add)
- ❌ File serving (need to add)

## Next Steps

1. Create build_service.py module
2. Enhance code_executor with build methods
3. Add build endpoints to server
4. Add file serving endpoints
5. Update INIT to trigger builds
6. Test with real React projects
