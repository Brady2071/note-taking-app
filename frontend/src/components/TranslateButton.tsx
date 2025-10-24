import React, { useState } from 'react';
import { apiService } from '../services/api';
import { TranslateRequest } from '../types/Note';
import './TranslateButton.css';

interface TranslateButtonProps {
  noteId: number;
  onTranslate: (title: string, content: string) => void;
  disabled?: boolean;
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

const TranslateButton: React.FC<TranslateButtonProps> = ({ noteId, onTranslate, disabled = false }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');

  const handleTranslate = async () => {
    if (!selectedLanguage) return;

    setIsTranslating(true);
    try {
      const request: TranslateRequest = { targetLang: selectedLanguage };
      const response = await apiService.translateNote(noteId, request);
      onTranslate(response.title, response.content);
      setIsOpen(false);
    } catch (error) {
      console.error('Translation failed:', error);
      alert('Translation failed. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="translate-button-container">
      <button
        className="translate-btn"
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled || isTranslating}
        title="Translate note"
      >
        🌐 {isTranslating ? 'Translating...' : 'Translate'}
      </button>
      
      {isOpen && (
        <div className="translate-dropdown">
          <div className="translate-header">
            <h4>Select Language</h4>
            <button 
              className="close-btn"
              onClick={() => setIsOpen(false)}
            >
              ×
            </button>
          </div>
          
          <div className="language-list">
            {SUPPORTED_LANGUAGES.map((lang) => (
              <button
                key={lang.code}
                className={`language-option ${selectedLanguage === lang.code ? 'selected' : ''}`}
                onClick={() => setSelectedLanguage(lang.code)}
              >
                {lang.name}
              </button>
            ))}
          </div>
          
          <div className="translate-actions">
            <button
              className="translate-action-btn"
              onClick={handleTranslate}
              disabled={isTranslating}
            >
              {isTranslating ? 'Translating...' : 'Translate'}
            </button>
            <button
              className="cancel-btn"
              onClick={() => setIsOpen(false)}
              disabled={isTranslating}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslateButton;
