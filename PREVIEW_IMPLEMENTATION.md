# Simple Preview Implementation

## What Was Implemented

A simple preview system that serves generated React code using:
- **React 18** from CDN (unpkg)
- **Babel Standalone** for JSX transpilation
- **FastAPI endpoint** at `/preview/{session_id}`

## How It Works

1. When a session is initialized, the backend returns a preview URL: `https://your-backend-url/preview/{session_id}`
2. The frontend iframe loads this URL
3. The `/preview/{session_id}` endpoint:
   - Loads code files from the database/file system
   - Finds `App.tsx` or `App.jsx`
   - Generates an HTML page with React from CDN
   - Uses Babel to transpile JSX in the browser
   - Renders the App component

## Configuration Required

Set the `BACKEND_URL` environment variable in Railway:

```
BACKEND_URL=https://website-ai-2-production.up.railway.app
```

This tells the backend what URL to use for preview links.

## Limitations

This is a **simple solution** with limitations:

### ✅ Works For:
- Simple React components
- JSX syntax
- React hooks (useState, useEffect, etc.)
- Basic styling

### ❌ Doesn't Support:
- Import statements (no bundler)
- npm packages (only React is loaded)
- TypeScript types (JSX only)
- Complex file structures
- CSS modules
- Build-time processing

## Future Improvements

For a production-ready preview, consider:
1. **Build Service**: Run `npm install` and `npm run build` on code changes
2. **Static File Serving**: Serve built `dist/` folders
3. **CodeSandbox/StackBlitz Integration**: Use existing code execution services
4. **Docker Containers**: Isolated environments per session
5. **Vite Dev Server**: Serve via Vite's dev server in development mode

## Testing

1. Create a session
2. Send a message like "Create a simple counter app with useState"
3. The preview should load in the iframe
4. The code should render and be interactive

## Example Generated Code

The preview endpoint generates HTML like this:

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        // User's App component code here
        function App() {
            const [count, setCount] = React.useState(0);
            return (
                <div>
                    <button onClick={() => setCount(count + 1)}>
                        Count: {count}
                    </button>
                </div>
            );
        }
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(React.createElement(App));
    </script>
</body>
</html>
```

This is a good starting point for previews!
