/**
 * Cloudflare Worker to proxy requests to Python backend
 * 
 * This worker forwards:
 * - HTTP requests to your Python FastAPI backend
 * - WebSocket connections to your Python backend
 */

export interface Env {
  // Backend URL (set in Cloudflare dashboard or wrangler.toml)
  BACKEND_URL: string;
  
  // Optional: API key for authentication
  API_KEY?: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    const backendUrl = env.BACKEND_URL;

    if (!backendUrl) {
      return new Response('BACKEND_URL not configured', { status: 500 });
    }

    // Handle WebSocket upgrade requests
    if (request.headers.get('Upgrade') === 'websocket') {
      return handleWebSocket(request, backendUrl);
    }

    // Handle regular HTTP requests
    return handleHTTP(request, backendUrl, env);
  },
};

/**
 * Handle HTTP requests (GET, POST, etc.)
 */
async function handleHTTP(
  request: Request,
  backendUrl: string,
  env: Env
): Promise<Response> {
  const url = new URL(request.url);
  
  // Construct backend URL
  const backendURL = new URL(url.pathname + url.search, backendUrl);
  
  // Create new request with same method and headers
  const headers = new Headers(request.headers);
  
  // Add CORS headers
  headers.set('Access-Control-Allow-Origin', '*');
  headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Forward request to backend
  const backendRequest = new Request(backendURL.toString(), {
    method: request.method,
    headers: headers,
    body: request.body,
  });

  try {
    const response = await fetch(backendRequest);
    
    // Create response with CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    // Clone response and add CORS headers
    const newResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: {
        ...Object.fromEntries(response.headers),
        ...corsHeaders,
      },
    });

    return newResponse;
  } catch (error) {
    console.error('Backend request failed:', error);
    return new Response(
      JSON.stringify({ error: 'Backend unavailable', message: String(error) }),
      {
        status: 502,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}

/**
 * Handle WebSocket connections
 * Note: Cloudflare Workers have limited WebSocket support
 * For full WebSocket support, you may need Durable Objects
 */
async function handleWebSocket(request: Request, backendUrl: string): Promise<Response> {
  // Extract WebSocket URL from request
  const url = new URL(request.url);
  const wsBackendUrl = url.pathname.replace('/ws', '') + '/ws';
  const backendWsUrl = new URL(wsBackendUrl, backendUrl);
  
  // Convert http/https to ws/wss
  const protocol = backendWsUrl.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${backendWsUrl.host}${backendWsUrl.pathname}${backendWsUrl.search}`;

  // For now, return a redirect or error
  // Full WebSocket proxying requires Durable Objects or a different approach
  return new Response('WebSocket proxying requires Durable Objects. Please connect directly to backend.', {
    status: 426,
    headers: {
      'Upgrade': 'websocket',
      'Connection': 'Upgrade',
    },
  });
}

