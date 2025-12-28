"""
FastAPI benchmark application.

Minimal endpoint returning JSON payload for benchmarking.
Run with: uvicorn fastapi_app:app --host 127.0.0.1 --port 8003 --workers 4
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()

# Standard response payload
RESPONSE_DATA = {
    'status': 'ok',
    'message': 'Hello from FastAPI',
    'data': {
        'id': 12345,
        'username': 'alice_dev',
        'email': 'alice@example.com',
    },
}


@app.get('/')
async def index():
    """Root endpoint returning JSON (sync)."""
    return RESPONSE_DATA


@app.get('/async')
async def index_async():
    """Root endpoint returning JSON (async)."""
    return RESPONSE_DATA


@app.get('/orjson', response_class=ORJSONResponse)
async def index_orjson():
    """Root endpoint using ORJSONResponse for faster serialization."""
    return RESPONSE_DATA


@app.get('/health')
async def health():
    """Health check endpoint."""
    return {'status': 'healthy'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8003)
