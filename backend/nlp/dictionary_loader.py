# nlp/dictionary_loader.py
import json
import os
from pathlib import Path

class MalagasyDictionary:
    """
    Gestionnaire de dictionnaire Malagasy pour la validation des mots.
    Supporte plusieurs sources de données.
    """
    
    def __init__(self):
        self.words = set()
        self.definitions = {}
        self.load_dictionaries()
    
    def load_dictionaries(self):
        """Charge tous les dictionnaires disponibles"""
        # Méthode 1 : Dictionnaire de base (créé manuellement)
        self._load_base_dictionary()
        
        # Méthode 2 : Dictionnaire depuis fichier JSON (si disponible)
        self._load_json_dictionary()
        
        # Méthode 3 : Dictionnaire depuis fichier texte (si disponible)
        self._load_text_dictionary()
    
    def _load_base_dictionary(self):
        """
        Dictionnaire de base avec les mots courants.
        À enrichir progressivement.
        """
        base_words = [
            # Pronoms
            "aho", "ianao", "izy", "isika", "izahay", "ianareo", "izy ireo",
            
            # Verbes courants
            "manao", "mandeha", "mipetraka", "mihinana", "misotro",
            "manasa", "mandidy", "miteny", "milaza", "manontany",
            "mahita", "mahare", "mahalala", "mahafantatra",
            "matory", "mifoha", "miasa", "mianatra", "mampianatra",
            
            # Noms courants
            "trano", "vola", "sakafo", "rano", "divay",
            "tany", "vary", "hena", "mofo", "akoho",
            "ray", "reny", "zanaka", "rahalahy", "rahavavy",
            "mpianatra", "mpampianatra", "dokotera", "mpiasa",
            
            # Adjectifs
            "tsara", "ratsy", "lehibe", "kely", "lava",
            "fohy", "mainty", "fotsy", "mena", "manga",
            "mafana", "mangatsiaka", "maina", "lena",
            
            # Prépositions et conjonctions
            "amin'ny", "eo", "any", "aty", "avy", "ho",
            "sy", "na", "fa", "kanefa", "nefa", "satria",
            
            # Mots interrogatifs
            "ahoana", "iza", "inona", "aiza", "rahoviana", "nahoana",
            
            # Temps
            "omaly", "androany", "rahampitso", "maraina", "hariva",
            "alina", "andro", "volana", "taona",
            
            # Nombres
            "iray", "roa", "telo", "efatra", "dimy",
            "enina", "fito", "valo", "sivy", "folo",
            
            # Autres mots fréquents
            "tsy", "tsia", "eny", "mety", "tonga", "lasa",
            "vita", "mbola", "efa", "dia", "koa", "ihany"
        ]
        
        self.words.update(base_words)
        print(f" Dictionnaire de base chargé : {len(base_words)} mots")
    
    def _load_json_dictionary(self):
        """
        Charge un dictionnaire depuis un fichier JSON.
        Format attendu : {"mot": "définition", ...}
        """
        json_path = Path("data/malagasy_dict.json")
        
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.definitions.update(data)
                    self.words.update(data.keys())
                print(f" Dictionnaire JSON chargé : {len(data)} mots")
            except Exception as e:
                print(f"  Erreur lors du chargement du JSON : {e}")
        else:
            print(f"ℹ  Fichier {json_path} non trouvé")
    
    def _load_text_dictionary(self):
        """
        Charge un dictionnaire depuis un fichier texte.
        Format : un mot par ligne
        """
        txt_path = Path("data/malagasy_words.txt")
        
        if txt_path.exists():
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    words = [line.strip().lower() for line in f if line.strip()]
                    self.words.update(words)
                print(f" Dictionnaire texte chargé : {len(words)} mots")
            except Exception as e:
                print(f"  Erreur lors du chargement du texte : {e}")
        else:
            print(f"ℹ  Fichier {txt_path} non trouvé")
    
    def word_exists(self, word):
        """Vérifie si un mot existe dans le dictionnaire"""
        word_clean = word.lower().strip(".,!?;:\"'")
        return word_clean in self.words
    
    def get_definition(self, word):
        """Récupère la définition d'un mot (si disponible)"""
        word_clean = word.lower().strip(".,!?;:\"'")
        return self.definitions.get(word_clean, None)
    
    def add_word(self, word, definition=None):
        """Ajoute un mot au dictionnaire"""
        word_clean = word.lower().strip()
        self.words.add(word_clean)
        if definition:
            self.definitions[word_clean] = definition
    
    def save_to_json(self, filepath="data/malagasy_dict.json"):
        """Sauvegarde le dictionnaire en JSON"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.definitions, f, ensure_ascii=False, indent=2)
        print(f" Dictionnaire sauvegardé : {filepath}")
    
    def save_to_text(self, filepath="data/malagasy_words.txt"):
        """Sauvegarde la liste des mots en texte"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for word in sorted(self.words):
                f.write(f"{word}\n")
        print(f" Liste de mots sauvegardée : {filepath}")
    
    def get_statistics(self):
        """Retourne des statistiques sur le dictionnaire"""
        return {
            "total_words": len(self.words),
            "words_with_definitions": len(self.definitions),
            "coverage_percentage": (len(self.definitions) / len(self.words) * 100) if self.words else 0
        }


# ============================================================
# SCRAPER POUR WIKIPEDIA MALAGASY (Optionnel - à exécuter une fois)
# ============================================================

def scrape_wikipedia_malagasy(limit=1000):
    """
    Scrape les mots depuis Wikipedia Malagasy.
    À exécuter une seule fois pour créer le dictionnaire.
    """
    import requests
    from bs4 import BeautifulSoup
    
    words = set()
    
    try:
        # API Wikipedia pour obtenir des pages aléatoires
        url = "https://mg.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "format": "json",
            "list": "random",
            "rnnamespace": "0",  # Articles uniquement
            "rnlimit": min(limit, 500)  # Max 500 par requête
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if "query" in data and "random" in data["query"]:
            for page in data["query"]["random"]:
                title = page["title"].lower()
                # Extraire les mots du titre
                words.update(title.split())
        
        print(f" {len(words)} mots extraits de Wikipedia")
        
    except Exception as e:
        print(f" Erreur lors du scraping : {e}")
    
    return words


def scrape_bible_malagasy():
    """
    Alternative : extraire des mots depuis la Bible en Malagasy
    (Corpus public disponible)
    """
    # La Bible malagasy est disponible sur plusieurs sites
    # C'est un excellent corpus pour extraire du vocabulaire
    pass


# ============================================================
# SCRIPT D'INITIALISATION
# ============================================================

def initialize_dictionary():
    """
    Script pour initialiser le dictionnaire.
    À exécuter une seule fois au début du projet.
    """
    print(" Initialisation du dictionnaire Malagasy...\n")
    
    dictionary = MalagasyDictionary()
    
    # Option 1 : Scraper Wikipedia (décommenter si besoin)
    # print(" Scraping Wikipedia...")
    # wiki_words = scrape_wikipedia_malagasy(limit=1000)
    # for word in wiki_words:
    #     dictionary.add_word(word)
    
    # Sauvegarder
    dictionary.save_to_json()
    dictionary.save_to_text()
    
    # Statistiques
    stats = dictionary.get_statistics()
    print(f"\n Statistiques du dictionnaire :")
    print(f"   - Total de mots : {stats['total_words']}")
    print(f"   - Avec définitions : {stats['words_with_definitions']}")
    print(f"   - Couverture : {stats['coverage_percentage']:.1f}%")


# ============================================================
# INTÉGRATION AVEC symbolic.py
# ============================================================

def validate_with_dictionary(text, dictionary):
    """
    Valide les mots d'un texte avec le dictionnaire.
    À intégrer dans symbolic_check().
    """
    from rapidfuzz import fuzz, process
    
    suggestions = []
    words = text.split()
    
    for i, word in enumerate(words):
        word_clean = word.lower().strip(".,!?;:\"'")
        
        if not dictionary.word_exists(word_clean):
            # Mot inconnu - suggérer des corrections
            closest_matches = process.extract(
                word_clean, 
                list(dictionary.words), 
                scorer=fuzz.ratio,
                limit=3
            )
            
            # Filtrer les suggestions avec un score > 70
            good_matches = [m for m in closest_matches if m[1] > 70]
            
            if good_matches:
                suggestions.append({
                    "position": text.find(word),
                    "type": "dictionnaire",
                    "severity": "warning",
                    "message": f"Mot '{word}' inconnu",
                    "suggestion": f"Suggestions : {', '.join([m[0] for m in good_matches])}",
                    "word": word,
                    "alternatives": [m[0] for m in good_matches]
                })
    
    return suggestions


# Test du module
if __name__ == "__main__":
    # Initialiser le dictionnaire
    print("=== TEST DU DICTIONNAIRE MALAGASY ===\n")
    
    dictionary = MalagasyDictionary()
    
    # Tests
    test_words = ["manao", "aho", "blabla", "tsaara", "tsy"]
    
    for word in test_words:
        exists = dictionary.word_exists(word)
        status = "V" if exists else "X"
        print(f"{status} '{word}' : {exists}")
    
    # Test de validation
    print("\n=== TEST DE VALIDATION ===\n")
    test_text = "Manao ahoana ianao? Aho dia tsaara daholo."
    suggestions = validate_with_dictionary(test_text, dictionary)
    
    if suggestions:
        for sugg in suggestions:
            print(f"  {sugg['message']}")
            print(f"   → {sugg['suggestion']}\n")
    else:
        print(" Aucune erreur détectée")