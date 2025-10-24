import pytest
import json
import os
from app import app
from src.llm import translate_text, generate_structured_notes

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_translate_note_endpoint(client):
    """Test translating a note via API"""
    # First create a note
    note_data = {
        'title': 'Hello World',
        'content': 'This is a test note in English',
        'tags': ['test']
    }
    
    create_response = client.post('/api/notes',
                                data=json.dumps(note_data),
                                content_type='application/json')
    note_id = json.loads(create_response.data)['id']
    
    # Translate the note
    translate_data = {'targetLang': 'es'}
    response = client.post(f'/api/notes/{note_id}/translate',
                          data=json.dumps(translate_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'title' in data
    assert 'content' in data
    assert data['originalId'] == note_id

def test_generate_note_endpoint(client):
    """Test generating a note via API"""
    generate_data = {
        'input': 'Meeting with team tomorrow at 2 PM to discuss project timeline',
        'language': 'en'
    }
    
    response = client.post('/api/generate-note',
                          data=json.dumps(generate_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'title' in data
    assert 'content' in data
    assert 'tags' in data
    assert 'id' in data

def test_translate_text_direct(client):
    """Test direct text translation"""
    translate_data = {
        'title': 'Test Title',
        'content': 'This is test content',
        'targetLang': 'fr'
    }
    
    response = client.post('/api/translate',
                          data=json.dumps(translate_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'title' in data
    assert 'content' in data

def test_llm_translate_function():
    """Test LLM translate function directly"""
    # Mock test - in real scenario, you'd need GITHUB_TOKEN
    try:
        result = translate_text(
            text="Hello world",
            target_language="es",
            title="Test"
        )
        assert 'title' in result
        assert 'content' in result
    except Exception as e:
        # Expected if GITHUB_TOKEN not set
        assert "GITHUB_TOKEN" in str(e) or "API" in str(e)

def test_llm_generate_function():
    """Test LLM generate function directly"""
    try:
        result = generate_structured_notes(
            user_input="Meeting tomorrow at 2 PM",
            language="en"
        )
        assert 'title' in result
        assert 'content' in result
        assert 'tags' in result
    except Exception as e:
        # Expected if GITHUB_TOKEN not set
        assert "GITHUB_TOKEN" in str(e) or "API" in str(e)

def test_missing_github_token():
    """Test behavior when GITHUB_TOKEN is missing"""
    # Temporarily remove token
    original_token = os.environ.get('GITHUB_TOKEN')
    if 'GITHUB_TOKEN' in os.environ:
        del os.environ['GITHUB_TOKEN']
    
    try:
        from src.llm import LLMClient
        client = LLMClient()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "GITHUB_TOKEN" in str(e)
    finally:
        # Restore token
        if original_token:
            os.environ['GITHUB_TOKEN'] = original_token
