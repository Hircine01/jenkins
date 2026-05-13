from flask import Flask, jsonify
from datetime import datetime
import os


app = Flask(__name__)


@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat(),
        'service': 'backend-api',
        'version': os.getenv('VERSION', '1.0.0')
    })


@app.route('/api/message')
def message():
    return jsonify({
        'message': 'Hello from Python Flask backend!',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/info')
def info():
    return jsonify({
        'name': 'Training App Backend',
        'version': '1.0.0',
        'python_version': '3.11',
        'flask_version': '2.3.0'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
