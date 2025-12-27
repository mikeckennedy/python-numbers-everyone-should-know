"""
Flask benchmark application.

Minimal endpoint returning JSON payload for benchmarking.
Run with: gunicorn -w 4 -b 127.0.0.1:8001 flask_app:app
"""

from flask import Flask, jsonify

app = Flask(__name__)

# Standard response payload
RESPONSE_DATA = {
    'status': 'ok',
    'message': 'Hello from Flask',
    'data': {
        'id': 12345,
        'username': 'alice_dev',
        'email': 'alice@example.com',
    },
}


@app.route('/')
def index():
    """Root endpoint returning JSON."""
    return jsonify(RESPONSE_DATA)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=False)
