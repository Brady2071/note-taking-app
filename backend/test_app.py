import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_get_notes_empty(client):
    """Test getting notes when none exist"""
    response = client.get('/api/notes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_note(client):
    """Test creating a new note"""
    note_data = {
        'title': 'Test Note',
        'content': 'This is a test note',
        'tags': ['test', 'automated']
    }
    
    response = client.post('/api/notes', 
                          data=json.dumps(note_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == note_data['title']
    assert data['content'] == note_data['content']
    assert data['tags'] == note_data['tags']
    assert 'id' in data
    assert 'updatedAt' in data

def test_get_note_by_id(client):
    """Test getting a specific note by ID"""
    # First create a note
    note_data = {
        'title': 'Test Note for Get',
        'content': 'Content for get test',
        'tags': ['test']
    }
    
    create_response = client.post('/api/notes',
                                data=json.dumps(note_data),
                                content_type='application/json')
    note_id = json.loads(create_response.data)['id']
    
    # Now get the note
    response = client.get(f'/api/notes/{note_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == note_data['title']

def test_update_note(client):
    """Test updating a note"""
    # Create a note first
    note_data = {
        'title': 'Original Title',
        'content': 'Original content',
        'tags': ['original']
    }
    
    create_response = client.post('/api/notes',
                                data=json.dumps(note_data),
                                content_type='application/json')
    note_id = json.loads(create_response.data)['id']
    
    # Update the note
    update_data = {
        'title': 'Updated Title',
        'content': 'Updated content',
        'tags': ['updated']
    }
    
    response = client.put(f'/api/notes/{note_id}',
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == update_data['title']
    assert data['content'] == update_data['content']
    assert data['tags'] == update_data['tags']

def test_delete_note(client):
    """Test deleting a note"""
    # Create a note first
    note_data = {
        'title': 'Note to Delete',
        'content': 'This note will be deleted',
        'tags': ['delete']
    }
    
    create_response = client.post('/api/notes',
                                data=json.dumps(note_data),
                                content_type='application/json')
    note_id = json.loads(create_response.data)['id']
    
    # Delete the note
    response = client.delete(f'/api/notes/{note_id}')
    assert response.status_code == 200
    
    # Verify note is deleted
    get_response = client.get(f'/api/notes/{note_id}')
    assert get_response.status_code == 404

def test_search_notes(client):
    """Test searching notes"""
    # Create test notes
    notes = [
        {'title': 'Python Tutorial', 'content': 'Learn Python programming', 'tags': ['python']},
        {'title': 'JavaScript Guide', 'content': 'JavaScript fundamentals', 'tags': ['javascript']},
        {'title': 'Web Development', 'content': 'Full stack development with Python and JS', 'tags': ['web']}
    ]
    
    for note_data in notes:
        client.post('/api/notes',
                   data=json.dumps(note_data),
                   content_type='application/json')
    
    # Search for Python
    response = client.get('/api/notes/search?q=python')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) >= 1
    assert any('python' in note['title'].lower() or 'python' in note['content'].lower() 
              for note in data)

def test_get_nonexistent_note(client):
    """Test getting a note that doesn't exist"""
    response = client.get('/api/notes/99999')
    assert response.status_code == 404

def test_update_nonexistent_note(client):
    """Test updating a note that doesn't exist"""
    update_data = {'title': 'Updated'}
    response = client.put('/api/notes/99999',
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 404

def test_delete_nonexistent_note(client):
    """Test deleting a note that doesn't exist"""
    response = client.delete('/api/notes/99999')
    assert response.status_code == 404
