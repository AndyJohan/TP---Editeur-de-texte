import API_BASE_URL from './api';

class Lemmatizer {
  constructor() {
    this.cache = new Map();
  }

  /**
   * Trouve la racine d'un mot
   */
  async findRoot(word) {
    if (this.cache.has(word)) {
      return this.cache.get(word);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/lemmatize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word }),
      });

      const data = await response.json();
      
      const result = {
        original: data.original,
        root: data.root,
        prefix: data.prefix,
        suffix: data.suffix,
        has_prefix: data.has_prefix,
        has_suffix: data.has_suffix
      };
      
      this.cache.set(word, result);
      return result;
    } catch (error) {
      console.error('Erreur findRoot:', error);
      return {
        original: word,
        root: word,
        prefix: '',
        suffix: '',
        has_prefix: false,
        has_suffix: false
      };
    }
  }
}

export default Lemmatizer;