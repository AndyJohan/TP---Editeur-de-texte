// src/App.js
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
import NLPChecker from './services/NLPChecker';

function App() {
  const [content, setContent] = useState('');
  const [showSidePanel, setShowSidePanel] = useState(false);
  const [sidePanelContent, setSidePanelContent] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [currentWord, setCurrentWord] = useState('');
  const [cursorPosition, setCursorPosition] = useState(null);
  const [qualityScore, setQualityScore] = useState(null);
  const [isChecking, setIsChecking] = useState(false);
  const [allSuggestions, setAllSuggestions] = useState([]);
  const quillRef = useRef(null);

  // Services
  const spellChecker = useRef(new SpellChecker()).current;
  const autoComplete = useRef(new AutoComplete()).current;
  const translator = useRef(new Translator()).current;
  const sentimentAnalyzer = useRef(new SentimentAnalysis()).current;
  const lemmatizer = useRef(new Lemmatizer()).current;
  const nlpChecker = useRef(new NLPChecker()).current;

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

  // Vérification complète du texte (débounce)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (content && content.trim().length > 10) {
        checkTextComplete();
      }
    }, 2000); // Attendre 2 secondes après la dernière frappe

    return () => clearTimeout(timer);
  }, [content]);

  // Vérification complète NLP
  const checkTextComplete = async () => {
    const editor = quillRef.current?.getEditor();
    if (!editor) return;

    const text = editor.getText();
    if (!text.trim()) return;

    setIsChecking(true);

    try {
      const results = await nlpChecker.checkComplete(text);
      
      // Mettre à jour le score de qualité
      setQualityScore(results.quality_score);
      
      // Stocker toutes les suggestions pour l'affichage
      setAllSuggestions(results.suggestions);

      // Souligner les mots avec erreurs (optionnel)
      highlightErrors(results.suggestions);
      
      console.log('✅ Analyse complète:', results);
    } catch (error) {
      console.error('❌ Erreur analyse:', error);
    } finally {
      setIsChecking(false);
    }
  };

  // Souligner les erreurs dans le texte
  const highlightErrors = (suggestions) => {
    const editor = quillRef.current?.getEditor();
    if (!editor) return;

    // Retirer les anciens surlignages
    editor.formatText(0, editor.getLength(), 'background', false);

    // Ajouter les nouveaux surlignages
    suggestions.forEach(sugg => {
      if (sugg.position !== undefined && sugg.word) {
        const color = sugg.severity === 'error' ? '#ffcccc' : 
                     sugg.severity === 'warning' ? '#fff4cc' : '#e6f3ff';
        
        try {
          editor.formatText(sugg.position, sugg.word.length, 'background', color);
        } catch (e) {
          // Ignorer si la position est invalide
        }
      }
    });
  };

  // Gestion du changement de texte
  const handleChange = (value) => {
    setContent(value);
    
    // Vérification orthographique en temps réel du dernier mot
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const text = editor.getText();
      const words = text.split(/\s+/);
      
      const lastWord = words[words.length - 1]?.trim();
      if (lastWord && lastWord.length > 2) {
        checkLastWord(lastWord);
      }
    }
  };

  // Vérifier le dernier mot tapé
  const checkLastWord = async (word) => {
    try {
      const isCorrect = await spellChecker.checkWord(word);
      
      if (!isCorrect) {
        const corrections = await spellChecker.getSuggestions(word);
        if (corrections.length > 0) {
          setSuggestions(corrections.slice(0, 5));
          setCurrentWord(word);
        }
      } else {
        setSuggestions([]);
      }
    } catch (error) {
      console.error('Erreur vérification mot:', error);
    }
  };

  // Autocomplétion
  const handleKeyUp = async (e) => {
    const editor = quillRef.current?.getEditor();
    if (!editor) return;

    const selection = editor.getSelection();
    if (!selection) return;

    const text = editor.getText(0, selection.index);
    const words = text.split(/\s+/);
    const currentWord = words[words.length - 1];

    if (currentWord && currentWord.length > 2) {
      try {
        // Essayer l'autocomplétion
        const completions = await autoComplete.autocomplete(currentWord, 10);
        
        if (completions.length > 0) {
          setSuggestions(completions);
          setCurrentWord(currentWord);
          setCursorPosition(selection.index);
        }
      } catch (error) {
        console.error('Erreur autocomplétion:', error);
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
  const analyzeSentiment = async () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const text = editor.getText();
      
      try {
        const result = await sentimentAnalyzer.analyze(text);
        setSidePanelContent({
          type: 'sentiment',
          data: result
        });
        setShowSidePanel(true);
      } catch (error) {
        console.error('Erreur analyse sentiment:', error);
      }
    }
  };

  // Traduction d'un mot sélectionné
  const translateSelection = async () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const selection = editor.getSelection();
      if (selection && selection.length > 0) {
        const selectedText = editor.getText(selection.index, selection.length);
        
        try {
          const translation = await translator.translate(selectedText.trim());
          setSidePanelContent({
            type: 'translation',
            data: { 
              word: selectedText.trim(), 
              translation 
            }
          });
          setShowSidePanel(true);
        } catch (error) {
          console.error('Erreur traduction:', error);
        }
      } else {
        alert('Veuillez sélectionner un mot à traduire');
      }
    }
  };

  // Lemmatisation
  const lemmatizeText = async () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const selection = editor.getSelection();
      if (selection && selection.length > 0) {
        const selectedText = editor.getText(selection.index, selection.length);
        
        try {
          const result = await lemmatizer.findRoot(selectedText.trim());
          setSidePanelContent({
            type: 'lemmatization',
            data: result
          });
          setShowSidePanel(true);
        } catch (error) {
          console.error('Erreur lemmatisation:', error);
        }
      } else {
        alert('Veuillez sélectionner un mot à lemmatiser');
      }
    }
  };

  // Synthèse vocale
  const speakText = () => {
    const editor = quillRef.current?.getEditor();
    if (editor) {
      const text = editor.getText();
      if ('speechSynthesis' in window) {
        // Arrêter toute lecture en cours
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'fr-FR'; // Malagasy n'est pas disponible, utiliser français
        utterance.rate = 0.8;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
      } else {
        alert('La synthèse vocale n\'est pas supportée par votre navigateur');
      }
    }
  };

  // Afficher toutes les suggestions
  const showAllSuggestions = () => {
    setSidePanelContent({
      type: 'all_suggestions',
      data: {
        suggestions: allSuggestions,
        qualityScore: qualityScore
      }
    });
    setShowSidePanel(true);
  };

  // Calculer les statistiques
  const wordCount = content.split(/\s+/).filter(w => w.trim()).length;
  const charCount = content.replace(/<[^>]*>/g, '').length;
  const errorCount = allSuggestions.filter(s => s.severity === 'error').length;
  const warningCount = allSuggestions.filter(s => s.severity === 'warning').length;

  return (
    <div className="App">
      <header className="app-header">
        <h1>🇲🇬 Éditeur de Texte Malagasy IA</h1>
        <p>Institut Supérieur Polytechnique de Madagascar</p>
        {qualityScore && (
          <div className="quality-badge" style={{
            backgroundColor: qualityScore.score >= 80 ? '#10b981' : 
                           qualityScore.score >= 60 ? '#f59e0b' : '#ef4444',
            color: 'white',
            padding: '5px 15px',
            borderRadius: '20px',
            fontSize: '14px',
            fontWeight: 'bold'
          }}>
            Score: {qualityScore.score}/100 - {qualityScore.level}
          </div>
        )}
      </header>

      <div className="app-container">
        <div className="editor-section">
          <Toolbar 
            onAnalyzeSentiment={analyzeSentiment}
            onTranslate={translateSelection}
            onLemmatize={lemmatizeText}
            onSpeak={speakText}
            onCheckText={checkTextComplete}
            isChecking={isChecking}
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
                  💡 Soso-kevitra ho an'ny: <strong>{currentWord}</strong>
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
            <span>📝 Teny: {wordCount}</span>
            <span>✍️ Litera: {charCount}</span>
            {errorCount > 0 && <span style={{color: '#ef4444'}}>❌ Erreurs: {errorCount}</span>}
            {warningCount > 0 && <span style={{color: '#f59e0b'}}>⚠️ Avertissements: {warningCount}</span>}
            {allSuggestions.length > 0 && (
              <button onClick={showAllSuggestions} className="view-suggestions-btn">
                📋 Voir toutes les suggestions ({allSuggestions.length})
              </button>
            )}
            {isChecking && <span>🔄 Vérification en cours...</span>}
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
        <p style={{fontSize: '12px', opacity: 0.8}}>
          Powered by FastAPI + React | NLP Engine: symbolic + algorithmic
        </p>
      </footer>
    </div>
  );
}

export default App;