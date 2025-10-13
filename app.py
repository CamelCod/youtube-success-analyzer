"""
Flask Backend for YouTube Success Analyzer Web Interface
"""
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import subprocess
import json
import sys
import os
from pathlib import Path
import threading
import time

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_channel():
    """Run the YouTube analyzer with streaming output"""
    data = request.get_json()
    channel_url = data.get('channelUrl', '')
    
    if not channel_url:
        return jsonify({'error': 'No channel URL provided'}), 400
    
    def generate():
        """Stream the analysis progress"""
        try:
            # Run the Python script
            process = subprocess.Popen(
                [sys.executable, 'youtube_success_analyzer.py'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Send the URL and confirmation
            process.stdin.write(f"{channel_url}\n")
            process.stdin.write("y\n")
            process.stdin.flush()
            
            output_path = ''
            video_count = 0
            total_views = 0
            
            # Stream output
            for line in iter(process.stdout.readline, ''):
                if line:
                    # Parse output for progress updates
                    yield f"data: {json.dumps({'type': 'log', 'message': line.strip()})}\n\n"
                    
                    # Extract statistics from output
                    if 'Found' in line and 'videos' in line:
                        try:
                            video_count = int(line.split()[2])
                        except:
                            pass
                    
                    if 'Progress:' in line:
                        try:
                            percent = int(line.split('(')[1].split('%')[0])
                            yield f"data: {json.dumps({'type': 'progress', 'percent': percent})}\n\n"
                        except:
                            pass
                    
                    if 'All files saved to:' in line:
                        output_path = line.split('All files saved to:')[1].strip()
            
            process.stdin.close()
            process.wait()
            
            # Send completion message
            yield f"data: {json.dumps({'type': 'complete', 'outputPath': output_path, 'stats': {'videoCount': video_count, 'totalViews': '0'}})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/open-folder', methods=['POST'])
def open_folder():
    """Open the output folder in file explorer"""
    data = request.get_json()
    path = data.get('path', '')
    
    if not path or not os.path.exists(path):
        return jsonify({'error': 'Invalid path'}), 400
    
    try:
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', path])
        else:
            subprocess.run(['xdg-open', path])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running in production
    is_production = os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT')
    
    if not is_production:
        print("="*80)
        print("🎯 YouTube Success Analyzer - Web Interface")
        print("="*80)
        print("\n🌐 Starting web server...")
        print(f"📍 Open your browser to: http://localhost:{port}")
        print("\n💡 Press Ctrl+C to stop the server\n")
        print("="*80)
    
    app.run(debug=not is_production, host='0.0.0.0', port=port, threaded=True)
