import API_BASE_URL from './api';

class SentimentAnalysis {
  /**
   * Analyse le sentiment d'un texte
   */
  async analyze(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/sentiment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      
      return {
        sentiment: data.sentiment,
        emoji: data.emoji,
        score: data.score,
        positive_words: data.positive_words,
        negative_words: data.negative_words,
        confidence: data.confidence
      };
    } catch (error) {
      console.error('Erreur analyze sentiment:', error);
      return {
        sentiment: 'neutre',
        emoji: '😐',
        score: 0.5,
        positive_words: 0,
        negative_words: 0,
        confidence: 'faible'
      };
    }
  }
}

export default SentimentAnalysis;