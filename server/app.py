from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json
import random
import time
import os

app = Flask(__name__)
CORS(app)

# Sample log data
SAMPLE_LOGS = [
    "User login successful - 2024-01-15 10:30:45",
    "Database query executed - 2024-01-15 10:31:12",
    "API request processed - 2024-01-15 10:32:01",
    "File upload completed - 2024-01-15 10:33:25",
    "Cache miss detected - 2024-01-15 10:34:18",
    "Email sent successfully - 2024-01-15 10:35:42",
    "Payment processed - 2024-01-15 10:36:55",
    "Backup completed - 2024-01-15 10:37:33",
    "Security scan finished - 2024-01-15 10:38:47",
    "System maintenance started - 2024-01-15 10:39:21",
    "User logout - 2024-01-15 10:40:15",
    "Data export completed - 2024-01-15 10:41:08"
]

# Initialize Redis connection
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url)

@app.route('/logs', methods=['GET'])
def get_logs():
    """Get 3 random logs"""
    try:
        # Check if we're waiting for IO
        awaiting_io = redis_client.get('awaiting_io')
        if awaiting_io and awaiting_io.decode() == 'true':
            return jsonify({
                'status': 'waiting',
                'message': 'Waiting for user input before continuing...'
            }), 200
        
        # Get 3 random logs
        random_logs = random.sample(SAMPLE_LOGS, 3)
        
        return jsonify({
            'status': 'success',
            'logs': random_logs
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/io/start', methods=['POST'])
def start_io():
    """Start IO process - set awaiting_io flag"""
    try:
        redis_client.set('awaiting_io', 'true')
        return jsonify({
            'status': 'success',
            'message': 'IO process started. Please provide input.'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/io/write', methods=['POST'])
def write_io():
    """Write IO data and unblock the process"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Store the message in Redis
        redis_client.set('user_message', message)
        
        # Set awaiting_io to false to unblock the process
        redis_client.set('awaiting_io', 'false')
        
        return jsonify({
            'status': 'success',
            'message': 'IO completed successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/io/read', methods=['GET'])
def read_io():
    """Read the stored IO message"""
    try:
        message = redis_client.get('user_message')
        if message:
            return jsonify({
                'status': 'success',
                'message': message.decode()
            }), 200
        else:
            return jsonify({
                'status': 'not_found',
                'message': 'No message found'
            }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True) 