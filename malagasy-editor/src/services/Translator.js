// Service de traduction Malagasy <-> Français
class Translator {
  constructor() {
    // Dictionnaire bilingue
    this.dictionary = {
      // Malagasy vers Français
      'aho': 'je/moi',
      'ianao': 'tu/toi',
      'izy': 'il/elle',
      'isika': 'nous (inclusif)',
      'izahay': 'nous (exclusif)',
      'ianareo': 'vous',
      'trano': 'maison',
      'tany': 'terre/pays',
      'rano': 'eau',
      'vary': 'riz',
      'mofo': 'pain',
      'sakay': 'piment',
      'sira': 'sel',
      'fianakaviany': 'famille',
      'ray': 'père',
      'reny': 'mère',
      'zanaka': 'enfant',
      'anadahy': 'frère (pour une fille)',
      'anabavy': 'sœur (pour un garçon)',
      'be': 'grand/beaucoup',
      'kely': 'petit/peu',
      'tsara': 'bien/bon',
      'ratsy': 'mauvais',
      'mainty': 'noir',
      'fotsy': 'blanc',
      'mena': 'rouge',
      'manao': 'faire',
      'mandeha': 'aller/partir',
      'mipetraka': 'rester/habiter',
      'mihinana': 'manger',
      'misotro': 'boire',
      'matory': 'dormir',
      'mahita': 'voir/trouver',
      'mahare': 'entendre',
      'mahalala': 'savoir/connaître',
      'mahafantatra': 'savoir',
      'manoratra': 'écrire',
      'mamaky': 'lire',
      'mianatra': 'étudier/apprendre',
      'mampianatra': 'enseigner',
      'miasa': 'travailler',
      'mihira': 'chanter',
      'mandihy': 'danser',
      'milalao': 'jouer',
      'fitiavana': 'amour',
      'hasina': 'sacré/respect',
      'fahasoavana': 'grâce',
      'fahamarinana': 'vérité',
      'malagasy': 'malgache',
      'madagasikara': 'Madagascar',
      'tanindrazana': 'patrie',
      'andriamanitra': 'Dieu',
      'masina': 'saint/sacré',
      'baiboly': 'Bible',
      'fivavahana': 'prière',
      'hazo': 'arbre/bois',
      'voninkazo': 'fleur',
      'ravina': 'feuille',
      'vato': 'pierre',
      'alika': 'chien',
      'saka': 'chat',
      'vorona': 'oiseau',
      'trondro': 'poisson',
      'omby': 'bœuf/vache',
      'akoho': 'poule',
      'loha': 'tête',
      'maso': 'œil',
      'sofina': 'oreille',
      'orona': 'nez',
      'vava': 'bouche',
      'tanana': 'main/ville',
      'tongotra': 'pied/jambe',
      'fo': 'cœur',
      'taona': 'année',
      'volana': 'mois',
      'andro': 'jour',
      'ora': 'heure',
      'maraina': 'matin',
      'hariva': 'soir',
      'alina': 'nuit',
      'omaly': 'hier',
      'ankehitriny': 'maintenant',
      'rahampitso': 'demain',
      'salama': 'bonjour/salut',
      'veloma': 'au revoir',
      'misaotra': 'merci',
      'azafady': 'pardon/s\'il vous plaît'
    };

    // Dictionnaire inverse (Français vers Malagasy)
    this.reverseDictionary = {};
    for (let [mg, fr] of Object.entries(this.dictionary)) {
      const frenchWords = fr.split('/');
      for (let fw of frenchWords) {
        this.reverseDictionary[fw.trim()] = mg;
      }
    }
  }

  translate(word) {
    const cleanWord = word.toLowerCase().trim();
    
    // Malagasy vers Français
    if (this.dictionary[cleanWord]) {
      return this.dictionary[cleanWord];
    }
    
    // Français vers Malagasy
    if (this.reverseDictionary[cleanWord]) {
      return this.reverseDictionary[cleanWord];
    }

    return 'Traduction non trouvée';
  }
}

export default Translator;
