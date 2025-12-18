import React, { useState, useRef, useEffect } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './App.css';
import Toolbar from './components/Toolbar';
import SidePanel from './components/SidePanel';
import SpellChecker from './services/SpellChecker';
import AutoComplete from './services/AutoComplete';
import Translator from './services/Translator';
import SentimentAnalysis from './services/SentimentAnalysis';
import Lemmatizer from './services/Lemmatizer';

function App() {
  const [content, setContent] = useState('');
  const [showSidePanel, setShowSidePanel] = useState(false);
  const [sidePanelContent, setSidePanelContent] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [currentWord, setCurrentWord] = useState('');
  const [cursorPosition, setCursorPosition] = useState(null);
  const quillRef = useRef(null);

  const spellChecker = new SpellChecker();
  const autoComplete = new AutoComplete();
  const translator = new Translator();
  const sentimentAnalyzer = new SentimentAnalysis();
  const lemmatizer = new Lemmatizer();

  const modules = {
    toolbar: {
      container: '#toolbar',
    },
  };

  const formats = [
    'header', 'font', 'size',
    'bold', 'italic', 'underline', 'strike', 'blockquote',
    'list', 'bullet', 'indent',
    'link', 'image', 'color', 'background',
    'align'
  ];

  // Gestion du changement de texte
  const handleChange = (value) => {
    setContent(value);
    
    // Vérification orthographique en temps réel
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const text = editor.getText();
      const words = text.split(/\s+/);
      
      // Vérifier le dernier mot
      const lastWord = words[words.length - 1]?.trim();
      if (lastWord && lastWord.length > 2) {
        const isCorrect = spellChecker.checkWord(lastWord);
        if (!isCorrect) {
          const corrections = spellChecker.getSuggestions(lastWord);
          if (corrections.length > 0) {
            setSuggestions(corrections);
            setCurrentWord(lastWord);
          }
        } else {
          setSuggestions([]);
        }
      }
    }
  };

  // Autocomplétion
  const handleKeyUp = (e) => {
    const editor = quillRef.current?.getEditor();
    if (!editor) return;

    const selection = editor.getSelection();
    if (!selection) return;

    const text = editor.getText(0, selection.index);
    const words = text.split(/\s+/);
    const currentWord = words[words.length - 1];

    if (currentWord && currentWord.length > 2) {
      const predictions = autoComplete.predictNextWord(currentWord);
      if (predictions.length > 0) {
        setSuggestions(predictions);
        setCurrentWord(currentWord);
        setCursorPosition(selection.index);
      }
    }
  };

  // Applique une suggestion
  const applySuggestion = (suggestion) => {
    const editor = quillRef.current?.getEditor();
    if (!editor) return;

    const selection = editor.getSelection();
    if (selection) {
      const text = editor.getText(0, selection.index);
      const lastSpaceIndex = text.lastIndexOf(' ');
      const startIndex = lastSpaceIndex >= 0 ? lastSpaceIndex + 1 : 0;
      
      editor.deleteText(startIndex, selection.index - startIndex);
      editor.insertText(startIndex, suggestion + ' ');
      editor.setSelection(startIndex + suggestion.length + 1);
    }
    
    setSuggestions([]);
    setCurrentWord('');
  };

  // Analyse de sentiment
  const analyzeSentiment = () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const text = editor.getText();
      const result = sentimentAnalyzer.analyze(text);
      setSidePanelContent({
        type: 'sentiment',
        data: result
      });
      setShowSidePanel(true);
    }
  };

  // Traduction d'un mot sélectionné
  const translateSelection = () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const selection = editor.getSelection();
      if (selection && selection.length > 0) {
        const selectedText = editor.getText(selection.index, selection.length);
        const translation = translator.translate(selectedText.trim());
        setSidePanelContent({
          type: 'translation',
          data: { word: selectedText.trim(), translation }
        });
        setShowSidePanel(true);
      }
    }
  };

  // Lemmatisation
  const lemmatizeText = () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const selection = editor.getSelection();
      if (selection && selection.length > 0) {
        const selectedText = editor.getText(selection.index, selection.length);
        const root = lemmatizer.findRoot(selectedText.trim());
        setSidePanelContent({
          type: 'lemmatization',
          data: { word: selectedText.trim(), root }
        });
        setShowSidePanel(true);
      }
    }
  };

  // Synthèse vocale
  const speakText = () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const text = editor.getText();
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'mg-MG';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
      } else {
        alert('La synthèse vocale n\'est pas supportée par votre navigateur');
      }
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🇲🇬 Éditeur de Texte Malagasy IA</h1>
        <p>Institut Supérieur Polytechnique de Madagascar</p>
      </header>

      <div className="app-container">
        <div className="editor-section">
          <Toolbar 
            onAnalyzeSentiment={analyzeSentiment}
            onTranslate={translateSelection}
            onLemmatize={lemmatizeText}
            onSpeak={speakText}
          />
          
          <div className="editor-wrapper">
            <ReactQuill
              ref={quillRef}
              theme="snow"
              value={content}
              onChange={handleChange}
              onKeyUp={handleKeyUp}
              modules={modules}
              formats={formats}
              placeholder="Soraty eto ny lahatsoratra malagasy..."
            />
            
            {suggestions.length > 0 && (
              <div className="suggestions-dropdown">
                <div className="suggestions-header">
                  Soso-kevitra ho an'ny: <strong>{currentWord}</strong>
                </div>
                {suggestions.map((suggestion, index) => (
                  <div 
                    key={index}
                    className="suggestion-item"
                    onClick={() => applySuggestion(suggestion)}
                  >
                    {suggestion}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="stats-bar">
            <span>Teny: {content.split(/\s+/).filter(w => w).length}</span>
            <span>Litera: {content.replace(/<[^>]*>/g, '').length}</span>
          </div>
        </div>

        {showSidePanel && (
          <SidePanel 
            content={sidePanelContent}
            onClose={() => setShowSidePanel(false)}
          />
        )}
      </div>

      <footer className="app-footer">
        <p>Projet IA - TP Clinique 2025 | Éditeur Intelligent pour Langues Low-Resource</p>
      </footer>
    </div>
  );
}

export default App;
