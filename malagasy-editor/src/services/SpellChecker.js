// Service de vérification orthographique pour le Malagasy
class SpellChecker {
  constructor() {
    // Dictionnaire de base - peut être étendu avec scraping de tenymalagasy.org
    this.dictionary = new Set([
      'aho', 'ianao', 'izy', 'isika', 'izahay', 'ianareo',
      'ny', 'ilay', 'ity', 'io', 'ireo',
      'dia', 'fa', 'ary', 'sy', 'na', 'raha', 'satria', 'nefa',
      'tsy', 'tsia', 'eny', 'marina',
      'manao', 'mandeha', 'mipetraka', 'mihinana', 'misotro', 'matory',
      'mahita', 'mahare', 'mahalala', 'mahafantatra',
      'trano', 'tany', 'rano', 'vary', 'mofo', 'sakay', 'sira',
      'fianakaviany', 'ray', 'reny', 'zanaka', 'anadahy', 'anabavy',
      'be', 'kely', 'tsara', 'ratsy', 'fo', 'mainty', 'fotsy',
      'iray', 'roa', 'telo', 'efatra', 'dimy', 'enina', 'fito', 'valo',
      'ankehitriny', 'omaly', 'rahampitso', 'maraina', 'hariva', 'alina',
      'taona', 'volana', 'herinandro', 'andro', 'ora', 'minitra',
      'malagasy', 'madagasikara', 'tanindrazana',
      'fitiavana', 'hasina', 'fahasoavana', 'fahamarinana',
      'manoratra', 'mamaky', 'mianatra', 'mampianatra',
      'miasa', 'mihira', 'mandihy', 'milalao',
      'lehibe', 'madinika', 'lava', 'fohy',
      'antananarivo', 'toamasina', 'antsirabe', 'fianarantsoa',
      'andriamanitra', 'masina', 'baiboly', 'fivavahana',
      'hazo', 'voninkazo', 'ravina', 'vato',
      'alika', 'saka', 'vorona', 'trondro', 'omby', 'akoho',
      'loha', 'maso', 'sofina', 'orona', 'vava', 'tanana', 'tongotra'
    ]);

    this.invalidCombinations = ['nb', 'mk', 'dt', 'bp', 'sz', 'nk'];
    this.prefixes = ['mi', 'ma', 'man', 'mam', 'maha', 'mpan', 'fi', 'fan'];
    this.suffixes = ['ana', 'ina', 'na'];
  }

  checkWord(word) {
    const cleanWord = word.toLowerCase().trim();
    if (this.dictionary.has(cleanWord)) return true;
    for (let combo of this.invalidCombinations) {
      if (cleanWord.includes(combo)) return false;
    }
    for (let prefix of this.prefixes) {
      if (cleanWord.startsWith(prefix)) return true;
    }
    return false;
  }

  levenshteinDistance(str1, str2) {
    const m = str1.length, n = str2.length;
    const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        dp[i][j] = str1[i-1] === str2[j-1] ? dp[i-1][j-1] : 
          Math.min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+1);
      }
    }
    return dp[m][n];
  }

  getSuggestions(word) {
    const cleanWord = word.toLowerCase().trim();
    const suggestions = [];
    for (let dictWord of this.dictionary) {
      const distance = this.levenshteinDistance(cleanWord, dictWord);
      if (distance <= 2) suggestions.push({ word: dictWord, distance });
    }
    suggestions.sort((a, b) => a.distance - b.distance);
    return suggestions.slice(0, 5).map(s => s.word);
  }
}

export default SpellChecker;
