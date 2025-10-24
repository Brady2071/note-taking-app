import React from 'react';
import { Note } from '../types/Note';
import './NoteList.css';

interface NoteListProps {
  notes: Note[];
  selectedNoteId: number | null;
  onSelectNote: (note: Note) => void;
  onDeleteNote: (id: number) => void;
}

const NoteList: React.FC<NoteListProps> = ({ notes, selectedNoteId, onSelectNote, onDeleteNote }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="note-list">
      <div className="note-list-header">
        <h2>Notes ({notes.length})</h2>
      </div>
      <div className="note-list-content">
        {notes.length === 0 ? (
          <div className="empty-state">
            <p>No notes yet. Create your first note!</p>
          </div>
        ) : (
          notes.map((note) => (
            <div
              key={note.id}
              className={`note-item ${selectedNoteId === note.id ? 'selected' : ''}`}
              onClick={() => onSelectNote(note)}
            >
              <div className="note-item-header">
                <h3 className="note-title">{note.title || 'Untitled'}</h3>
                <button
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteNote(note.id);
                  }}
                  title="Delete note"
                >
                  ×
                </button>
              </div>
              <p className="note-preview">
                {note.content.substring(0, 100)}
                {note.content.length > 100 && '...'}
              </p>
              <div className="note-meta">
                <span className="note-date">{formatDate(note.updatedAt)}</span>
                {note.tags.length > 0 && (
                  <div className="note-tags">
                    {note.tags.map((tag, index) => (
                      <span key={index} className="tag">{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default NoteList;
