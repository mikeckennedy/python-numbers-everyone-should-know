"""
Litestar benchmark application.

Minimal endpoint returning JSON payload for benchmarking.
Run with: uvicorn litestar_app:app --host 127.0.0.1 --port 8005 --workers 4
"""

from litestar import Litestar, get

# Standard response payload
RESPONSE_DATA = {
    "status": "ok",
    "message": "Hello from Litestar",
    "data": {
        "id": 12345,
        "username": "alice_dev",
        "email": "alice@example.com",
    },
}


@get("/")
async def index() -> dict:
    """Root endpoint returning JSON."""
    return RESPONSE_DATA


@get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


app = Litestar([index, health])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8005)
