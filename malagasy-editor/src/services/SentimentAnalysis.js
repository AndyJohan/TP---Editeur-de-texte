// Service d'analyse de sentiment (Bag of Words)
class SentimentAnalysis {
  constructor() {
    // Mots positifs en Malagasy
    this.positiveWords = [
      'tsara', 'soa', 'mahafaly', 'sambatra', 'ravoravo',
      'mahafinaritra', 'mahagaga', 'mahatalanjona',
      'fitiavana', 'fahasoavana', 'hasina', 'mendrika',
      'marina', 'mahery', 'sarobidy', 'tena', 'be',
      'lehibe', 'masina', 'salama', 'misaotra',
      'finaritra', 'fahombiazana', 'voninahitra'
    ];

    // Mots négatifs en Malagasy
    this.negativeWords = [
      'ratsy', 'tsy', 'fadiranovana', 'alahelo', 'mampalahelo',
      'mahantra', 'kivy', 'malahelo', 'mampatahotra',
      'mampisedra', 'marary', 'mangidy', 'mangirifiry',
      'maharikoriko', 'tsy misy', 'very', 'simba',
      'fahoriana', 'fahantrana', 'faharahabariana'
    ];
  }

  analyze(text) {
    const cleanText = text.toLowerCase();
    const words = cleanText.split(/\s+/);
    
    let positiveCount = 0;
    let negativeCount = 0;
    const foundPositive = [];
    const foundNegative = [];

    // Compte les mots positifs et négatifs
    for (let word of words) {
      const cleanWord = word.replace(/[.,!?;:]/g, '').trim();
      
      if (this.positiveWords.includes(cleanWord)) {
        positiveCount++;
        if (!foundPositive.includes(cleanWord)) {
          foundPositive.push(cleanWord);
        }
      }
      
      if (this.negativeWords.includes(cleanWord)) {
        negativeCount++;
        if (!foundNegative.includes(cleanWord)) {
          foundNegative.push(cleanWord);
        }
      }
    }

    // Calcule le sentiment
    const total = positiveCount + negativeCount;
    let sentiment = 'neutral';
    let score = 50;

    if (total > 0) {
      score = Math.round((positiveCount / total) * 100);
      
      if (score > 60) {
        sentiment = 'positive';
      } else if (score < 40) {
        sentiment = 'negative';
      }
    }

    return {
      sentiment,
      score,
      positiveWords: foundPositive,
      negativeWords: foundNegative,
      positiveCount,
      negativeCount
    };
  }
}

export default SentimentAnalysis;
