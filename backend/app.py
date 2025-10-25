from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS for Vercel deployment
CORS(app, origins=[
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://note-taking-app-*.vercel.app"
])

# Try to import database modules, fallback if not available
try:
    from models import Note, SessionLocal
    from src.llm import translate_text, generate_structured_notes
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Database modules not available: {e}")
    DATABASE_AVAILABLE = False
    Note = None
    SessionLocal = None
    translate_text = None
    generate_structured_notes = None

def get_db():
    if not DATABASE_AVAILABLE or not SessionLocal:
        return None
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def close_db(db):
    if db:
        db.close()

@app.route('/notes', methods=['GET'])
def get_notes():
    if not DATABASE_AVAILABLE:
        # Return sample data when database is not available
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
    
    db = get_db()
    try:
        notes = db.query(Note).order_by(Note.updated_at.desc()).all()
        return jsonify([note.to_dict() for note in notes])
    finally:
        close_db(db)

@app.route('/notes', methods=['POST'])
def create_note():
    if not DATABASE_AVAILABLE:
        return jsonify({'message': 'Database not available. Please configure DATABASE_URL environment variable.'}), 503
    
    db = get_db()
    try:
        data = request.get_json()
        note = Note.from_dict(data)
        db.add(note)
        db.commit()
        db.refresh(note)
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        close_db(db)

@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    db = get_db()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(note.to_dict())
    finally:
        close_db(db)

@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    db = get_db()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json()
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.tags = json.dumps(data.get('tags', []))
        note.updated_at = datetime.utcnow()
        
        db.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        close_db(db)

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    db = get_db()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        db.delete(note)
        db.commit()
        return jsonify({'message': 'Note deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        close_db(db)

@app.route('/notes/search', methods=['GET'])
def search_notes():
    db = get_db()
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify([])
        
        notes = db.query(Note).filter(
            Note.title.contains(query) | Note.content.contains(query)
        ).order_by(Note.updated_at.desc()).all()
        
        return jsonify([note.to_dict() for note in notes])
    finally:
        close_db(db)

@app.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate a specific note"""
    db = get_db()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        data = request.get_json()
        target_language = data.get('targetLang', 'en')
        
        if not target_language:
            return jsonify({'error': 'targetLang is required'}), 400
        
        # Translate the note
        translated = translate_text(
            text=note.content,
            target_language=target_language,
            title=note.title
        )
        
        return jsonify({
            'title': translated['title'],
            'content': translated['content'],
            'originalId': note_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500
    finally:
        close_db(db)

@app.route('/translate', methods=['POST'])
def translate_text_direct():
    """Translate text directly without saving to database"""
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')
        target_language = data.get('targetLang', 'en')
        
        if not content:
            return jsonify({'error': 'content is required'}), 400
        
        if not target_language:
            return jsonify({'error': 'targetLang is required'}), 400
        
        # Translate the text
        translated = translate_text(
            text=content,
            target_language=target_language,
            title=title
        )
        
        return jsonify({
            'title': translated['title'],
            'content': translated['content']
        })
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@app.route('/generate-note', methods=['POST'])
def generate_note():
    """Generate a structured note from natural language input"""
    db = get_db()
    try:
        data = request.get_json()
        user_input = data.get('input', '')
        language = data.get('language', 'en')
        
        if not user_input:
            return jsonify({'error': 'input is required'}), 400
        
        # Generate structured note
        generated = generate_structured_notes(user_input, language)
        
        # Create note in database
        note = Note()
        note.title = generated['title']
        note.content = generated['content']
        note.tags = json.dumps(generated['tags'])
        note.event_date = generated.get('event_date')
        note.event_time = generated.get('event_time')
        
        db.add(note)
        db.commit()
        db.refresh(note)
        
        return jsonify(note.to_dict()), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': f'Note generation failed: {str(e)}'}), 500
    finally:
        close_db(db)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
