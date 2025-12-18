// Service d'autocomplétion avec N-grams
class AutoComplete {
  constructor() {
    // Bigrammes fréquents en Malagasy
    this.bigrams = {
      'ny': ['aho', 'olona', 'trano', 'tanana', 'fiainana'],
      'dia': ['mandeha', 'miasa', 'mipetraka', 'tsara'],
      'manao': ['ahoana', 'inona', 'izany'],
      'tsy': ['misy', 'mahalala', 'mahafantatra', 'tsara'],
      'fa': ['tsy', 'marina', 'tsara'],
      'izy': ['dia', 'ireo', 'no'],
      'malagasy': ['dia', 'ny', 'tsara'],
      'tsara': ['loatra', 'dia', 'be'],
      'mandeha': ['any', 'aho', 'isika'],
      'miasa': ['aho', 'izy', 'isika'],
      'mipetraka': ['eto', 'aho'],
      'mahafantatra': ['ny', 'aho'],
      'mahita': ['azy', 'ny']
    };

    // Phrases communes
    this.commonPhrases = [
      'salama ianareo',
      'misaotra betsaka',
      'azafady tompoko',
      'veloma aho',
      'tonga soa',
      'manao ahoana',
      'tsara fa tsara',
      'ny fiainana',
      'ny tanindrazana',
      'madagasikara sambatra'
    ];
  }

  predictNextWord(currentWord) {
    const word = currentWord.toLowerCase().trim();
    
    // Cherche dans les bigrammes
    if (this.bigrams[word]) {
      return this.bigrams[word];
    }

    // Cherche dans les phrases communes
    const matching = this.commonPhrases
      .filter(phrase => phrase.startsWith(word))
      .map(phrase => phrase.split(' ')[0]);

    if (matching.length > 0) {
      return [...new Set(matching)];
    }

    // Suggestions par défaut basées sur les préfixes
    if (word.startsWith('mi')) {
      return ['miasa', 'mihira', 'mianatra', 'mihinana', 'misotro'];
    }
    if (word.startsWith('ma')) {
      return ['manao', 'mandeha', 'mahita', 'mahalala', 'mahafantatra'];
    }
    if (word.startsWith('fi')) {
      return ['fiainana', 'fianakaviany', 'fitiavana', 'fivavahana'];
    }

    return [];
  }
}

export default AutoComplete;
