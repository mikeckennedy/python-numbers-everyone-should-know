"""
Starlette benchmark application.

Minimal endpoint returning JSON payload for benchmarking.
Run with: uvicorn starlette_app:app --host 127.0.0.1 --port 8004 --workers 4
"""

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Standard response payload
RESPONSE_DATA = {
    'status': 'ok',
    'message': 'Hello from Starlette',
    'data': {
        'id': 12345,
        'username': 'alice_dev',
        'email': 'alice@example.com',
    },
}


async def index(request):
    """Root endpoint returning JSON."""
    return JSONResponse(RESPONSE_DATA)


async def health(request):
    """Health check endpoint."""
    return JSONResponse({'status': 'healthy'})


routes = [
    Route('/', index),
    Route('/health', health),
]

app = Starlette(routes=routes)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8004)
