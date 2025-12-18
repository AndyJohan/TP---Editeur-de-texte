import React from 'react';
import './Toolbar.css';

const Toolbar = ({ onAnalyzeSentiment, onTranslate, onLemmatize, onSpeak }) => {
  return (
    <div className="custom-toolbar">
      <div id="toolbar">
        <span className="ql-formats">
          <select className="ql-header" defaultValue="">
            <option value="1">Lohateny 1</option>
            <option value="2">Lohateny 2</option>
            <option value="3">Lohateny 3</option>
            <option value="">Normal</option>
          </select>
        </span>
        
        <span className="ql-formats">
          <button className="ql-bold" title="Matotra" />
          <button className="ql-italic" title="Mitongilana" />
          <button className="ql-underline" title="Tsipika" />
          <button className="ql-strike" title="Voatsipika" />
        </span>
        
        <span className="ql-formats">
          <select className="ql-color" title="Lokon-tsoratra" />
          <select className="ql-background" title="Lokon-tsipika" />
        </span>
        
        <span className="ql-formats">
          <button className="ql-list" value="ordered" title="Lisitra misy isa" />
          <button className="ql-list" value="bullet" title="Lisitra" />
          <select className="ql-align" title="Fampitoviana" />
        </span>
        
        <span className="ql-formats">
          <button className="ql-link" title="Rohy" />
          <button className="ql-image" title="Sary" />
        </span>
      </div>
      
      <div className="ai-toolbar">
        <button className="ai-button" onClick={onAnalyzeSentiment} title="Famakafakana fihetseham-po">
          😊 Sentiment
        </button>
        <button className="ai-button" onClick={onTranslate} title="Fandikana (Malagasy ↔ Français)">
          🌐 Dika
        </button>
        <button className="ai-button" onClick={onLemmatize} title="Fakany">
          🔍 Faka
        </button>
        <button className="ai-button" onClick={onSpeak} title="Vakio">
          🔊 Vakio
        </button>
      </div>
    </div>
  );
};

export default Toolbar;
