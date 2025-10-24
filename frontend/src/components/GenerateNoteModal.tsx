import React, { useState } from 'react';
import { apiService } from '../services/api';
import { GenerateNoteRequest } from '../types/Note';
import './GenerateNoteModal.css';

interface GenerateNoteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onNoteGenerated: (note: any) => void;
}

const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'zh', name: '中文' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'ja', name: '日本語' },
  { code: 'ko', name: '한국어' },
  { code: 'pt', name: 'Português' },
  { code: 'ru', name: 'Русский' },
  { code: 'ar', name: 'العربية' }
];

const GenerateNoteModal: React.FC<GenerateNoteModalProps> = ({ isOpen, onClose, onNoteGenerated }) => {
  const [input, setInput] = useState('');
  const [language, setLanguage] = useState('en');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!input.trim()) return;

    setIsGenerating(true);
    try {
      const request: GenerateNoteRequest = { 
        input: input.trim(), 
        language 
      };
      const note = await apiService.generateNote(request);
      onNoteGenerated(note);
      setInput('');
      onClose();
    } catch (error) {
      console.error('Note generation failed:', error);
      alert('Note generation failed. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleClose = () => {
    if (!isGenerating) {
      setInput('');
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Generate Note</h3>
          <button 
            className="close-btn"
            onClick={handleClose}
            disabled={isGenerating}
          >
            ×
          </button>
        </div>
        
        <div className="modal-body">
          <div className="form-group">
            <label htmlFor="language-select">Language:</label>
            <select
              id="language-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              disabled={isGenerating}
            >
              {SUPPORTED_LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="note-input">Describe what you want to note:</label>
            <textarea
              id="note-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="e.g., Meeting with team tomorrow at 2 PM to discuss project timeline and deliverables"
              disabled={isGenerating}
              rows={4}
            />
          </div>
        </div>
        
        <div className="modal-footer">
          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={!input.trim() || isGenerating}
          >
            {isGenerating ? 'Generating...' : 'Generate Note'}
          </button>
          <button
            className="cancel-btn"
            onClick={handleClose}
            disabled={isGenerating}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default GenerateNoteModal;
