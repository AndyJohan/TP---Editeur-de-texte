import API_BASE_URL from './api';

class AutoComplete {
  constructor() {
    this.cache = new Map();
  }

  /**
   * Autocomplétion d'un préfixe
   */
  async autocomplete(prefix, limit = 10) {
    if (prefix.length < 2) {
      return [];
    }

    const cacheKey = `${prefix}-${limit}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/autocomplete?prefix=${encodeURIComponent(prefix)}&limit=${limit}`
      );

      const data = await response.json();
      const suggestions = data.suggestions || [];
      
      this.cache.set(cacheKey, suggestions);
      return suggestions;
    } catch (error) {
      console.error('Erreur autocomplete:', error);
      return [];
    }
  }

  /**
   * Prédiction du mot suivant
   */
  async predictNextWord(context, limit = 5) {
    try {
      // Si context est une string, la diviser en mots
      const contextArray = Array.isArray(context) 
        ? context 
        : context.split(/\s+/).filter(w => w.trim());

      if (contextArray.length === 0) {
        return [];
      }

      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          context: contextArray,
          limit 
        }),
      });

      const data = await response.json();
      
      // Retourner juste les mots (compatibilité avec l'ancien code)
      return data.predictions?.map(p => p.word) || [];
    } catch (error) {
      console.error('Erreur predictNextWord:', error);
      return [];
    }
  }
}

export default AutoComplete;

