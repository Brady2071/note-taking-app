import os
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from app import app
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback to simple app if backend import fails
    from flask import Flask, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app, origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://note-taking-app-*.vercel.app"
    ])
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Note-taking app is running!'})
    
    @app.route('/notes', methods=['GET'])
    def get_notes():
        return jsonify({'message': 'Database integration pending'})

# This is the entry point for Vercel
if __name__ == "__main__":
    app.run()
