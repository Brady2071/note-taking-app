import React, { useState, useEffect, useCallback } from 'react';
import { Note, CreateNoteRequest, UpdateNoteRequest } from './types/Note';
import { apiService } from './services/api';
import NoteList from './components/NoteList';
import NoteEditor from './components/NoteEditor';
import SearchBar from './components/SearchBar';
import GenerateNoteModal from './components/GenerateNoteModal';
import './App.css';

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [filteredNotes, setFilteredNotes] = useState<Note[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isGenerateModalOpen, setIsGenerateModalOpen] = useState(false);

  const loadNotes = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const fetchedNotes = await apiService.getNotes();
      setNotes(fetchedNotes);
      setFilteredNotes(fetchedNotes);
    } catch (err) {
      setError('Failed to load notes. Please check if the backend is running.');
      console.error('Error loading notes:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const searchNotes = useCallback(async (query: string) => {
    try {
      const searchResults = await apiService.searchNotes(query);
      setFilteredNotes(searchResults);
    } catch (err) {
      console.error('Error searching notes:', err);
      // Fallback to client-side filtering
      const filtered = notes.filter(note =>
        note.title.toLowerCase().includes(query.toLowerCase()) ||
        note.content.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredNotes(filtered);
    }
  }, [notes]);

  // Load notes on component mount
  useEffect(() => {
    loadNotes();
  }, []);

  // Filter notes based on search query
  useEffect(() => {
    if (searchQuery.trim()) {
      searchNotes(searchQuery);
    } else {
      setFilteredNotes(notes);
    }
  }, [searchQuery, notes, searchNotes]);

  const handleSelectNote = (note: Note) => {
    setSelectedNote(note);
  };

  const handleSaveNote = async (noteData: CreateNoteRequest | UpdateNoteRequest) => {
    try {
      setIsSaving(true);
      setError(null);

      let savedNote: Note;
      if (selectedNote) {
        // Update existing note
        savedNote = await apiService.updateNote(selectedNote.id, noteData);
        setNotes(prevNotes =>
          prevNotes.map(note => note.id === selectedNote.id ? savedNote : note)
        );
        setSelectedNote(savedNote);
      } else {
        // Create new note
        savedNote = await apiService.createNote(noteData as CreateNoteRequest);
        setNotes(prevNotes => [savedNote, ...prevNotes]);
        setSelectedNote(savedNote);
      }
    } catch (err) {
      setError('Failed to save note. Please try again.');
      console.error('Error saving note:', err);
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeleteNote = async (id: number) => {
    try {
      setError(null);
      await apiService.deleteNote(id);
      setNotes(prevNotes => prevNotes.filter(note => note.id !== id));
      
      if (selectedNote && selectedNote.id === id) {
        setSelectedNote(null);
      }
    } catch (err) {
      setError('Failed to delete note. Please try again.');
      console.error('Error deleting note:', err);
    }
  };

  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
  };

  const handleClearSearch = () => {
    setSearchQuery('');
  };

  const handleNewNote = () => {
    setSelectedNote(null);
  };

  const handleNoteGenerated = (note: Note) => {
    setNotes(prevNotes => [note, ...prevNotes]);
    setSelectedNote(note);
    setIsGenerateModalOpen(false);
  };

  if (isLoading) {
    return (
      <div className="app">
        <div className="loading">
          <p>Loading notes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>Notes</h1>
          <div className="header-actions">
            <button 
              className="generate-note-btn" 
              onClick={() => setIsGenerateModalOpen(true)}
            >
              ✨ Generate
            </button>
            <button className="new-note-btn" onClick={handleNewNote}>
              + New Note
            </button>
          </div>
        </div>
        <SearchBar
          searchQuery={searchQuery}
          onSearchChange={handleSearchChange}
          onClearSearch={handleClearSearch}
        />
        <NoteList
          notes={filteredNotes}
          selectedNoteId={selectedNote?.id || null}
          onSelectNote={handleSelectNote}
          onDeleteNote={handleDeleteNote}
        />
      </div>
      <div className="main-content">
        {error && (
          <div className="error-banner">
            <p>{error}</p>
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}
        <NoteEditor
          selectedNote={selectedNote}
          onSaveNote={handleSaveNote}
          onDeleteNote={handleDeleteNote}
          isSaving={isSaving}
        />
      </div>
      
      <GenerateNoteModal
        isOpen={isGenerateModalOpen}
        onClose={() => setIsGenerateModalOpen(false)}
        onNoteGenerated={handleNoteGenerated}
      />
    </div>
  );
}

export default App;
