import API_BASE_URL from './api';

class SpellChecker {
  constructor() {
    this.cache = new Map();
  }

  /**
   * Vérifie l'orthographe d'un texte complet
   */
  async checkText(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la vérification');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur SpellChecker:', error);
      return {
        suggestions: [],
        statistics: {},
        quality_score: { score: 0, level: 'Erreur' }
      };
    }
  }

  /**
   * Vérifie un mot unique
   */
  async checkWord(word) {
    if (this.cache.has(word)) {
      return this.cache.get(word);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/word-info`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word }),
      });

      const data = await response.json();
      const isCorrect = data.exists;
      
      this.cache.set(word, isCorrect);
      return isCorrect;
    } catch (error) {
      console.error('Erreur checkWord:', error);
      return true;
    }
  }

  /**
   * Obtient des suggestions pour un mot incorrect
   */
  async getSuggestions(word) {
    try {
      const response = await fetch(`${API_BASE_URL}/word-info`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word }),
      });

      const data = await response.json();
      return data.suggestions || [];
    } catch (error) {
      console.error('Erreur getSuggestions:', error);
      return [];
    }
  }
}

export default SpellChecker;
