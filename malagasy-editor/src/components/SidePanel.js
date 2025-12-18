import React from 'react';
import './SidePanel.css';

const SidePanel = ({ content, onClose }) => {
  const renderContent = () => {
    if (!content) return null;

    switch (content.type) {
      case 'sentiment':
        return (
          <div className="panel-content">
            <h3>📊 Famakafakana Fihetseham-po</h3>
            <div className="sentiment-result">
              <div className={`sentiment-badge ${content.data.sentiment}`}>
                {content.data.sentiment === 'positive' ? '😊 Tsara' : 
                 content.data.sentiment === 'negative' ? '😞 Ratsy' : 
                 '😐 Tsy miankina'}
              </div>
              <div className="sentiment-score">
                <div className="score-bar">
                  <div 
                    className={`score-fill ${content.data.sentiment}`}
                    style={{ width: `${content.data.score}%` }}
                  />
                </div>
                <span>{content.data.score}%</span>
              </div>
              <div className="sentiment-details">
                <p><strong>Teny tsara:</strong> {content.data.positiveWords.join(', ') || 'Tsy misy'}</p>
                <p><strong>Teny ratsy:</strong> {content.data.negativeWords.join(', ') || 'Tsy misy'}</p>
              </div>
            </div>
          </div>
        );

      case 'translation':
        return (
          <div className="panel-content">
            <h3>🌐 Fandikana</h3>
            <div className="translation-result">
              <div className="word-pair">
                <div className="source-word">
                  <span className="label">Malagasy:</span>
                  <span className="word">{content.data.word}</span>
                </div>
                <div className="arrow">→</div>
                <div className="target-word">
                  <span className="label">Français:</span>
                  <span className="word">{content.data.translation}</span>
                </div>
              </div>
            </div>
          </div>
        );

      case 'lemmatization':
        return (
          <div className="panel-content">
            <h3>🔍 Fakany</h3>
            <div className="lemma-result">
              <div className="word-pair">
                <div className="source-word">
                  <span className="label">Teny:</span>
                  <span className="word">{content.data.word}</span>
                </div>
                <div className="arrow">→</div>
                <div className="target-word">
                  <span className="label">Faka:</span>
                  <span className="word">{content.data.root}</span>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="side-panel">
      <button className="close-button" onClick={onClose}>✕</button>
      {renderContent()}
    </div>
  );
};

export default SidePanel;
