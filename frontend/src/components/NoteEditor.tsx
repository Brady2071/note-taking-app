import React, { useState, useEffect } from 'react';
import { Note, CreateNoteRequest, UpdateNoteRequest } from '../types/Note';
import TranslateButton from './TranslateButton';
import './NoteEditor.css';

interface NoteEditorProps {
  selectedNote: Note | null;
  onSaveNote: (note: CreateNoteRequest | UpdateNoteRequest) => Promise<void>;
  onDeleteNote: (id: number) => Promise<void>;
  isSaving: boolean;
}

const NoteEditor: React.FC<NoteEditorProps> = ({ 
  selectedNote, 
  onSaveNote, 
  onDeleteNote, 
  isSaving 
}) => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');

  useEffect(() => {
    if (selectedNote) {
      setTitle(selectedNote.title);
      setContent(selectedNote.content);
      setTags(selectedNote.tags);
    } else {
      setTitle('');
      setContent('');
      setTags([]);
    }
  }, [selectedNote]);

  const handleSave = async () => {
    if (!title.trim() && !content.trim()) return;

    const noteData = {
      title: title.trim() || 'Untitled',
      content: content.trim(),
      tags: tags
    };

    await onSaveNote(noteData);
  };

  const handleDelete = async () => {
    if (selectedNote && window.confirm('Are you sure you want to delete this note?')) {
      await onDeleteNote(selectedNote.id);
    }
  };

  const addTag = () => {
    const newTag = tagInput.trim();
    if (newTag && !tags.includes(newTag)) {
      setTags([...tags, newTag]);
      setTagInput('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSave();
    }
  };

  const handleTranslate = (translatedTitle: string, translatedContent: string) => {
    setTitle(translatedTitle);
    setContent(translatedContent);
  };

  return (
    <div className="note-editor">
      <div className="note-editor-header">
        <input
          type="text"
          className="note-title-input"
          placeholder="Note title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <div className="note-editor-actions">
          {selectedNote && (
            <TranslateButton
              noteId={selectedNote.id}
              onTranslate={handleTranslate}
              disabled={isSaving}
            />
          )}
          <button
            className="save-btn"
            onClick={handleSave}
            disabled={isSaving || (!title.trim() && !content.trim())}
          >
            {isSaving ? 'Saving...' : 'Save'}
          </button>
          {selectedNote && (
            <button
              className="delete-btn"
              onClick={handleDelete}
              disabled={isSaving}
            >
              Delete
            </button>
          )}
        </div>
      </div>

      <div className="tags-section">
        <div className="tags-input">
          <input
            type="text"
            placeholder="Add tag..."
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                addTag();
              }
            }}
          />
          <button onClick={addTag} disabled={!tagInput.trim()}>
            Add
          </button>
        </div>
        <div className="tags-list">
          {tags.map((tag, index) => (
            <span key={index} className="tag">
              {tag}
              <button onClick={() => removeTag(tag)}>×</button>
            </span>
          ))}
        </div>
      </div>

      <textarea
        className="note-content-input"
        placeholder="Start writing your note..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        onKeyPress={handleKeyPress}
      />

      <div className="note-editor-footer">
        <small>Press Ctrl+Enter to save</small>
      </div>
    </div>
  );
};

export default NoteEditor;
