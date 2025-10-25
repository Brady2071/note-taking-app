from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://note-taking-app-*.vercel.app"
])

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Note-taking app is running!'})

@app.route('/api/notes', methods=['GET'])
def get_notes():
    # Return sample data for now
    sample_notes = [
        {
            'id': 1,
            'title': 'Welcome to Note-Taking App',
            'content': 'This is a sample note. The app is successfully deployed on Vercel!',
            'tags': ['welcome', 'sample'],
            'eventDate': None,
            'eventTime': None,
            'updatedAt': '2024-01-01T00:00:00Z'
        },
        {
            'id': 2,
            'title': 'Deployment Success',
            'content': 'Your note-taking app has been successfully deployed to Vercel with Apple-inspired design!',
            'tags': ['deployment', 'success'],
            'eventDate': None,
            'eventTime': None,
            'updatedAt': '2024-01-01T00:00:00Z'
        }
    ]
    return jsonify(sample_notes)

@app.route('/api/notes', methods=['POST'])
def create_note():
    return jsonify({'message': 'Note creation endpoint ready - database integration pending'})

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    return jsonify({'message': f'Get note {note_id} endpoint ready'})

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    return jsonify({'message': f'Update note {note_id} endpoint ready'})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    return jsonify({'message': f'Delete note {note_id} endpoint ready'})

@app.route('/api/notes/search', methods=['GET'])
def search_notes():
    return jsonify({'message': 'Search endpoint ready'})

if __name__ == "__main__":
    app.run()

