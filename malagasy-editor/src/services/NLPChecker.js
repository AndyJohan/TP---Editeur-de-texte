import API_BASE_URL from './api';

class NLPChecker {
  /**
   * Analyse complète d'un texte
   */
  async checkComplete(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error('Erreur lors de l\'analyse');
      }

      const data = await response.json();
      
      return {
        suggestions: data.suggestions || [],
        suggestions_by_category: data.suggestions_by_category || {},
        statistics: data.statistics || {},
        quality_score: data.quality_score || { score: 0, level: 'Inconnu' },
        analysis: data.analysis || {},
      };
    } catch (error) {
      console.error('Erreur checkComplete:', error);
      return {
        suggestions: [],
        suggestions_by_category: {},
        statistics: {},
        quality_score: { score: 0, level: 'Erreur' },
        analysis: {},
      };
    }
  }

  /**
   * Obtient les statistiques du dictionnaire
   */
  async getStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getStats:', error);
      return null;
    }
  }
}

export default NLPChecker;