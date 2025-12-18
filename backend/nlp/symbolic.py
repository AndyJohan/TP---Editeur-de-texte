# nlp/symbolic.py (VERSION INTÉGRÉE AVEC DICTIONNAIRE)
import re
from backend.nlp.dictionary_loader import MalagasyDictionary, validate_with_dictionary

# Charger le dictionnaire une seule fois (au démarrage)
DICTIONARY = MalagasyDictionary()

def symbolic_check(text):
    """
    Analyse le texte pour détecter les erreurs symboliques selon des règles linguistiques malagasy.
    Retourne une liste de suggestions avec justification.
    """
    suggestions = []
    words = text.split()
    
    # ============================================================
    # Règle 1 : Combinaisons phonotactiques interdites en Malagasy
    # ============================================================
    forbidden_combinations = {
        "nb": "Utiliser 'mb' à la place",
        "mk": "Vérifier l'orthographe - 'mk' n'existe pas",
        "dt": "Utiliser 'd' ou 't' séparément",
        "bp": "Utiliser 'b' ou 'p' séparément",
        "sz": "Utiliser 's' ou 'z' séparément"
    }
    
    for comb, suggestion in forbidden_combinations.items():
        pattern = re.compile(comb, re.IGNORECASE)
        for match in pattern.finditer(text):
            suggestions.append({
                "position": match.start(),
                "type": "phonotactique",
                "severity": "error",
                "message": f"Combinaison interdite '{comb}' détectée",
                "suggestion": suggestion,
                "word": _get_word_at_position(text, match.start())
            })
    
    # ============================================================
    # Règle 2 : Validation des préfixes courants
    # ============================================================
    valid_prefixes = {
        "mi-": ["mitory", "milaza", "mihinana"],
        "ma-": ["mahay", "mahita", "manana"],
        "man-": ["manao", "manome", "mandray"],
        "mam-": ["mamaky", "mamindra", "mamita"],
        "maha-": ["mahafaly", "mahagaga"],
        "mpan-": ["mpanao", "mpandray"],
        "mpam-": ["mpamaky", "mpamindra"],
        "fi-": ["fihaoana", "fitiavana"],
        "fan-": ["fanao", "fanomezana"],
        "fam-": ["famakiana", "famindrana"],
        "tsy": ["tsy", "tsisy"]
    }
    
    for i, word in enumerate(words):
        word_lower = word.lower().strip(".,!?;:")
        
        for prefix in valid_prefixes.keys():
            if word_lower.startswith(prefix):
                root = word_lower[len(prefix):]
                
                if len(root) < 2:
                    suggestions.append({
                        "position": text.find(word),
                        "type": "morphologie",
                        "severity": "warning",
                        "message": f"Préfixe '{prefix}' sur racine trop courte",
                        "suggestion": f"Vérifier le mot '{word}' - racine incomplète",
                        "word": word
                    })
    
    # ============================================================
    # Règle 3 : Validation des suffixes courants
    # ============================================================
    valid_suffixes = {
        "-ana": "nominalisation/lieu",
        "-ina": "passif/impératif",
        "-na": "passif court",
        "-itra": "résultat d'action",
        "-nana": "possession abstraite"
    }
    
    for i, word in enumerate(words):
        word_lower = word.lower().strip(".,!?;:")
        
        for suffix, meaning in valid_suffixes.items():
            if word_lower.endswith(suffix):
                root = word_lower[:-len(suffix)]
                
                if len(root) < 2:
                    suggestions.append({
                        "position": text.find(word),
                        "type": "morphologie",
                        "severity": "warning",
                        "message": f"Suffixe '{suffix}' sur racine trop courte",
                        "suggestion": f"Vérifier le mot '{word}' - racine incomplète",
                        "word": word
                    })
    
    # ============================================================
    # Règle 4 : Doublons de voyelles non-standards
    # ============================================================
    double_vowel_pattern = re.compile(r'([aeiou])\1{2,}', re.IGNORECASE)
    
    for match in double_vowel_pattern.finditer(text):
        suggestions.append({
            "position": match.start(),
            "type": "orthographe",
            "severity": "warning",
            "message": f"Triple voyelle '{match.group()}' détectée",
            "suggestion": "Vérifier l'orthographe - peu commun en Malagasy",
            "word": _get_word_at_position(text, match.start())
        })
    
    # ============================================================
    # Règle 5 : Mots commençant par 'nk' (rare en début de mot)
    # ============================================================
    for i, word in enumerate(words):
        word_lower = word.lower()
        if word_lower.startswith("nk") and len(word_lower) > 2:
            suggestions.append({
                "position": text.find(word),
                "type": "phonotactique",
                "severity": "warning",
                "message": f"Mot commençant par 'nk' : '{word}'",
                "suggestion": "Vérifier - 'nk' en début de mot est rare",
                "word": word
            })
    
    # ============================================================
    # Règle 6 : Lettres non-malagasy (w, c, q, u isolé, x)
    # ============================================================
    non_malagasy_letters = re.compile(r'\b\w*[wqx]\w*\b', re.IGNORECASE)
    
    for match in non_malagasy_letters.finditer(text):
        word = match.group()
        suggestions.append({
            "position": match.start(),
            "type": "orthographe",
            "severity": "warning",
            "message": f"Lettre non-standard détectée dans '{word}'",
            "suggestion": "Vérifier l'orthographe - w, q, x sont rares en Malagasy",
            "word": word
        })
    
    # ============================================================
    # Règle 7 : Validation avec le dictionnaire (Levenshtein)
    # ============================================================
    dict_suggestions = validate_with_dictionary(text, DICTIONARY)
    suggestions.extend(dict_suggestions)
    
    # ============================================================
    # Règle 8 : Détection de mélange de langues (optionnel)
    # ============================================================
    foreign_indicators = {
        "le": "français", "la": "français", "les": "français",
        "the": "anglais", "is": "anglais", "are": "anglais",
        "et": "français", "ou": "français"
    }
    
    for i, word in enumerate(words):
        word_lower = word.lower().strip(".,!?;:")
        if word_lower in foreign_indicators:
            # Ne pas signaler si le mot existe aussi en malagasy
            if not DICTIONARY.word_exists(word_lower):
                suggestions.append({
                    "position": text.find(word),
                    "type": "langue",
                    "severity": "info",
                    "message": f"Mot '{word}' semble être en {foreign_indicators[word_lower]}",
                    "suggestion": "Vérifier si c'est intentionnel",
                    "word": word
                })
    
    return suggestions


def _get_word_at_position(text, position):
    """Récupère le mot complet à une position donnée dans le texte."""
    start = position
    end = position
    
    while start > 0 and text[start - 1].isalnum():
        start -= 1
    
    while end < len(text) and text[end].isalnum():
        end += 1
    
    return text[start:end]


def get_severity_color(severity):
    """Retourne une couleur pour l'affichage selon la gravité."""
    colors = {
        "error": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    }
    return colors.get(severity, "#6b7280")


# ============================================================
# TESTS
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE L'ANALYSEUR SYMBOLIQUE MALAGASY")
    print("=" * 60)
    
    # Afficher les stats du dictionnaire
    stats = DICTIONARY.get_statistics()
    print(f"\n Dictionnaire chargé : {stats['total_words']} mots")
    print("=" * 60)
    
    test_texts = [
        "Manao ahoana ianao",                    #  Correct
        "Mihinana sakafo aho",                   #  Correct
        "Tsy mankany aho",                       #  Correct
        "Le livre est nbien",                    #  combinaison interdite + français
        "Miana fitiavana",                       #  préfixe court
        "Tsaara daholo",                         #  faute d'orthographe (devrait être 'tsara')
        "Nkomba vaovao",                         #  commence par nk
        "Maxime aaa dia lasa",                   #  triple voyelle + nom étranger
        "Mamaky boky sy manoratra",              #  Correct
        "Blabla xyz qwerty"                      #  Mots inconnus + lettres non-malagasy
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}.  Texte: '{text}'")
        print("-" * 60)
        
        results = symbolic_check(text)
        
        if results:
            # Grouper par type
            errors = [r for r in results if r['severity'] == 'error']
            warnings = [r for r in results if r['severity'] == 'warning']
            infos = [r for r in results if r['severity'] == 'info']
            
            if errors:
                print(f"    ERREURS ({len(errors)}):")
                for sugg in errors:
                    print(f"      [{sugg['type']}] {sugg['message']}")
                    print(f"      → {sugg['suggestion']}")
            
            if warnings:
                print(f"     AVERTISSEMENTS ({len(warnings)}):")
                for sugg in warnings:
                    print(f"      [{sugg['type']}] {sugg['message']}")
                    print(f"      → {sugg['suggestion']}")
                    if 'alternatives' in sugg:
                        print(f"       Suggestions: {', '.join(sugg['alternatives'])}")
            
            if infos:
                print(f"   ℹ  INFORMATIONS ({len(infos)}):")
                for sugg in infos:
                    print(f"      [{sugg['type']}] {sugg['message']}")
        else:
            print("    Aucune erreur détectée")
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)