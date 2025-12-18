// Service de lemmatisation pour le Malagasy
class Lemmatizer {
  constructor() {
    // Préfixes à retirer
    this.prefixes = [
      'maha', 'mpan', 'mpam', 'man', 'mam', 'mi', 'ma',
      'fan', 'fam', 'fi', 'f', 'an', 'am', 'i'
    ];

    // Suffixes à retirer
    this.suffixes = [
      'ana', 'ina', 'na', 'any', 'a'
    ];

    // Racines connues
    this.knownRoots = {
      'manoratra': 'soratra',
      'manao': 'ao',
      'mandeha': 'deha',
      'mihinana': 'hina',
      'misotro': 'sotro',
      'matory': 'tory',
      'mahita': 'hita',
      'mahare': 'hare',
      'mahalala': 'halala',
      'mahafantatra': 'fantatra',
      'mianatra': 'ianatra',
      'mampianatra': 'ianatra',
      'miasa': 'asa',
      'mihira': 'hira',
      'mandihy': 'dihy',
      'milalao': 'lalao',
      'mamaky': 'vaky',
      'manosika': 'tosika',
      'manokatra': 'sokatra',
      'manidy': 'hidy',
      'mandoko': 'loko',
      'manadio': 'madio',
      'mividy': 'vidy',
      'mivarotra': 'varotra',
      'mandoa': 'doa',
      'mandray': 'ray'
    };
  }

  findRoot(word) {
    const cleanWord = word.toLowerCase().trim();

    // Vérifie si la racine est connue
    if (this.knownRoots[cleanWord]) {
      return this.knownRoots[cleanWord];
    }

    let root = cleanWord;

    // Retire les préfixes (du plus long au plus court)
    for (let prefix of this.prefixes.sort((a, b) => b.length - a.length)) {
      if (root.startsWith(prefix) && root.length > prefix.length + 2) {
        root = root.substring(prefix.length);
        break;
      }
    }

    // Retire les suffixes (du plus long au plus court)
    for (let suffix of this.suffixes.sort((a, b) => b.length - a.length)) {
      if (root.endsWith(suffix) && root.length > suffix.length + 2) {
        root = root.substring(0, root.length - suffix.length);
        break;
      }
    }

    return root;
  }

  // Décompose un mot en préfixe + racine + suffixe
  decompose(word) {
    const cleanWord = word.toLowerCase().trim();
    let prefix = '';
    let root = cleanWord;
    let suffix = '';

    // Trouve le préfixe
    for (let p of this.prefixes.sort((a, b) => b.length - a.length)) {
      if (root.startsWith(p)) {
        prefix = p;
        root = root.substring(p.length);
        break;
      }
    }

    // Trouve le suffixe
    for (let s of this.suffixes.sort((a, b) => b.length - a.length)) {
      if (root.endsWith(s)) {
        suffix = s;
        root = root.substring(0, root.length - s.length);
        break;
      }
    }

    return { prefix, root, suffix };
  }
}

export default Lemmatizer;
