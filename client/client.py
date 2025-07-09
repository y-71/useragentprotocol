from flask import Flask, render_template_string, request, jsonify
import requests
import os
import time

app = Flask(__name__)

SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:3000')

# Simple HTML template for the client interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Log Client</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .log-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .log-item { background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 3px; }
        .io-section { background: #e8f4fd; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #0056b3; }
        input[type="text"] { padding: 10px; width: 300px; margin: 10px 0; }
        .status { padding: 10px; margin: 10px 0; border-radius: 3px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .waiting { background: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Log Client</h1>
        
        <div class="log-section">
            <h2>Current Logs</h2>
            <button onclick="getLogs()">Get Logs</button>
            <div id="logs"></div>
        </div>
        
        <div class="io-section">
            <h2>IO Operations</h2>
            <button onclick="startIO()">Start IO Process</button>
            <br><br>
            <input type="text" id="messageInput" placeholder="Enter your message">
            <button onclick="writeIO()">Send Message</button>
            <div id="ioStatus"></div>
        </div>
        
        <div class="log-section">
            <h2>Stored Message</h2>
            <button onclick="readIO()">Read Stored Message</button>
            <div id="storedMessage"></div>
        </div>
    </div>

    <script>
        async function getLogs() {
            try {
                const response = await fetch('/api/logs');
                const data = await response.json();
                
                const logsDiv = document.getElementById('logs');
                if (data.status === 'waiting') {
                    logsDiv.innerHTML = '<div class="status waiting">' + data.message + '</div>';
                } else if (data.status === 'success') {
                    let html = '<div class="status success">Logs retrieved successfully:</div>';
                    data.logs.forEach(log => {
                        html += '<div class="log-item">' + log + '</div>';
                    });
                    logsDiv.innerHTML = html;
                } else {
                    logsDiv.innerHTML = '<div class="status error">Error: ' + data.error + '</div>';
                }
            } catch (error) {
                document.getElementById('logs').innerHTML = '<div class="status error">Error: ' + error.message + '</div>';
            }
        }

        async function startIO() {
            try {
                const response = await fetch('/api/io/start', { method: 'POST' });
                const data = await response.json();
                
                const statusDiv = document.getElementById('ioStatus');
                if (data.status === 'success') {
                    statusDiv.innerHTML = '<div class="status success">' + data.message + '</div>';
                } else {
                    statusDiv.innerHTML = '<div class="status error">Error: ' + data.error + '</div>';
                }
            } catch (error) {
                document.getElementById('ioStatus').innerHTML = '<div class="status error">Error: ' + error.message + '</div>';
            }
        }

        async function writeIO() {
            const message = document.getElementById('messageInput').value;
            if (!message) {
                alert('Please enter a message');
                return;
            }

            try {
                const response = await fetch('/api/io/write', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                
                const statusDiv = document.getElementById('ioStatus');
                if (data.status === 'success') {
                    statusDiv.innerHTML = '<div class="status success">' + data.message + '</div>';
                    document.getElementById('messageInput').value = '';
                } else {
                    statusDiv.innerHTML = '<div class="status error">Error: ' + data.error + '</div>';
                }
            } catch (error) {
                document.getElementById('ioStatus').innerHTML = '<div class="status error">Error: ' + error.message + '</div>';
            }
        }

        async function readIO() {
            try {
                const response = await fetch('/api/io/read');
                const data = await response.json();
                
                const messageDiv = document.getElementById('storedMessage');
                if (data.status === 'success') {
                    messageDiv.innerHTML = '<div class="status success">Stored message: ' + data.message + '</div>';
                } else if (data.status === 'not_found') {
                    messageDiv.innerHTML = '<div class="status waiting">' + data.message + '</div>';
                } else {
                    messageDiv.innerHTML = '<div class="status error">Error: ' + data.error + '</div>';
                }
            } catch (error) {
                document.getElementById('storedMessage').innerHTML = '<div class="status error">Error: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/logs')
def get_logs():
    """Proxy to server logs endpoint"""
    try:
        response = requests.get(f"{SERVER_URL}/logs")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/io/start', methods=['POST'])
def start_io():
    """Proxy to server IO start endpoint"""
    try:
        response = requests.post(f"{SERVER_URL}/io/start")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/io/write', methods=['POST'])
def write_io():
    """Proxy to server IO write endpoint"""
    try:
        data = request.get_json()
        response = requests.post(f"{SERVER_URL}/io/write", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/io/read')
def read_io():
    """Proxy to server IO read endpoint"""
    try:
        response = requests.get(f"{SERVER_URL}/io/read")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 