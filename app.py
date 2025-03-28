from flask import Flask, request, jsonify
import subprocess
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    filename = f"audio_{uuid.uuid4()}.mp3"
    command = ['yt-dlp', '-x', '--audio-format', 'mp3', '-o', filename, url]
    subprocess.run(command)
    return jsonify({'mp3_url': f'https://your-host.com/{filename}'})