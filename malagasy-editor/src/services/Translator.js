import API_BASE_URL from './api';

class Translator {
  constructor() {
    this.cache = new Map();
  }

  /**
   * Traduit un mot
   */
  async translate(word, direction = 'mg-fr') {
    const cacheKey = `${word}-${direction}`;
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ word, direction }),
      });

      const data = await response.json();
      
      if (data.found) {
        this.cache.set(cacheKey, data.translation);
        return data.translation;
      }
      
      return 'Traduction non disponible';
    } catch (error) {
      console.error('Erreur translate:', error);
      return 'Erreur de traduction';
    }
  }
}

export default Translator;