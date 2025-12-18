# nlp/nlp_checker.py
"""
API complète d'analyse de texte Malagasy
Combine les modules symbolic et algorithmic
"""

from backend.nlp.symbolic import symbolic_check
from backend.nlp.algorithmic import (
    SpellChecker, 
    MalagasyLemmatizer,
    NGramModel,
    SentenceAnalyzer,
    SentenceValidator
)
from backend.nlp.dictionary_loader import MalagasyDictionary
from typing import Dict, List

# Charger le dictionnaire et les modèles une seule fois
DICTIONARY = MalagasyDictionary()
LEMMATIZER = MalagasyLemmatizer()
ANALYZER = SentenceAnalyzer()
VALIDATOR = SentenceValidator()

# Charger le modèle N-gram (si disponible)
try:
    NGRAM_MODEL = NGramModel(n=2)
    NGRAM_MODEL.load_model("data/ngram_model.json")
    print(" Modèle N-gram chargé")
except:
    NGRAM_MODEL = None
    print("ℹ  Modèle N-gram non disponible (entraîner d'abord)")


def check_text_complete(text: str) -> Dict:
    """
    Analyse complète d'un texte Malagasy
    Combine toutes les vérifications (symbolic + algorithmic)
    
    Args:
        text: Texte à analyser
    
    Returns:
        Dict avec toutes les analyses et suggestions
    """
    
    if not text or not text.strip():
        return {
            "error": "Texte vide",
            "suggestions": []
        }
    
    results = {
        "text": text,
        "suggestions": [],
        "analysis": {},
        "statistics": {}
    }
    
    # ============================================================
    # 1. VÉRIFICATIONS SYMBOLIQUES (Règles linguistiques)
    # ============================================================
    symbolic_suggestions = symbolic_check(text)
    
    # Formater les suggestions symboliques
    for sugg in symbolic_suggestions:
        results["suggestions"].append({
            "type": sugg["type"],
            "severity": sugg["severity"],
            "position": sugg["position"],
            "word": sugg["word"],
            "message": sugg["message"],
            "suggestion": sugg["suggestion"],
            "category": "symbolic"
        })
    
    # ============================================================
    # 2. CORRECTION ORTHOGRAPHIQUE (Levenshtein)
    # ============================================================
    spell_checker = SpellChecker(DICTIONARY.words)
    spelling_errors = spell_checker.correct_text(text)
    
    for error in spelling_errors:
        results["suggestions"].append({
            "type": "spelling",
            "severity": "warning",
            "position": error["position"],
            "word": error["original"],
            "message": f"Mot '{error['original']}' possiblement mal orthographié",
            "suggestion": f"Suggestions: {', '.join(error['suggestions'][:3])}",
            "alternatives": error["suggestions"],
            "category": "algorithmic"
        })
    
    # ============================================================
    # 3. VALIDATION DE STRUCTURE DE PHRASE
    # ============================================================
    sentences = ANALYZER.split_sentences(text)
    
    for sentence in sentences:
        sentence_validation = VALIDATOR.validate_sentence(sentence)
        
        for validation in sentence_validation:
            results["suggestions"].append({
                "type": validation["type"],
                "severity": validation["severity"],
                "position": text.find(sentence),
                "word": sentence[:30] + "..." if len(sentence) > 30 else sentence,
                "message": validation["message"],
                "suggestion": validation["suggestion"],
                "category": "structure"
            })
    
    # ============================================================
    # 4. ANALYSE DE PHRASES
    # ============================================================
    sentence_analysis = ANALYZER.analyze_text(text)
    results["analysis"]["sentences"] = sentence_analysis
    
    # ============================================================
    # 5. LEMMATISATION
    # ============================================================
    lemmatization_results = LEMMATIZER.lemmatize_text(text)
    results["analysis"]["lemmatization"] = lemmatization_results
    
    # ============================================================
    # 6. STATISTIQUES
    # ============================================================
    words = text.split()
    unique_words = set(w.lower().strip(".,!?;:\"'") for w in words)
    
    results["statistics"] = {
        "total_words": len(words),
        "unique_words": len(unique_words),
        "total_sentences": len(sentences),
        "average_sentence_length": sentence_analysis.get("average_words", 0),
        "vso_compliance": sentence_analysis.get("vso_percentage", 0),
        "complex_sentences": sentence_analysis.get("complex_sentences", 0),
        "total_suggestions": len(results["suggestions"]),
        "errors": len([s for s in results["suggestions"] if s["severity"] == "error"]),
        "warnings": len([s for s in results["suggestions"] if s["severity"] == "warning"]),
        "info": len([s for s in results["suggestions"] if s["severity"] == "info"])
    }
    
    return results


def get_next_word_predictions(context: List[str], top_k: int = 5) -> List[Dict]:
    """
    Prédit les mots suivants possibles
    
    Args:
        context: Liste des mots précédents
        top_k: Nombre de prédictions
    
    Returns:
        Liste de prédictions avec probabilités
    """
    if not NGRAM_MODEL:
        return []
    
    predictions = NGRAM_MODEL.predict_next_word(context, top_k)
    
    return [
        {
            "word": word,
            "probability": prob,
            "confidence": f"{prob:.1%}"
        }
        for word, prob in predictions
    ]


def autocomplete_word(prefix: str, top_k: int = 5) -> List[str]:
    """
    Suggère des complétions pour un préfixe
    
    Args:
        prefix: Début du mot
        top_k: Nombre de suggestions
    
    Returns:
        Liste de mots possibles
    """
    if not NGRAM_MODEL:
        # Fallback : chercher dans le dictionnaire
        prefix_lower = prefix.lower()
        matches = [
            word for word in DICTIONARY.words 
            if word.startswith(prefix_lower)
        ]
        return sorted(matches)[:top_k]
    
    return NGRAM_MODEL.autocomplete(prefix, top_k)


def get_word_info(word: str) -> Dict:
    """
    Obtient toutes les informations sur un mot
    
    Args:
        word: Mot à analyser
    
    Returns:
        Dict avec lemmatisation, validation, définition
    """
    word_clean = word.lower().strip(".,!?;:\"'")
    
    info = {
        "word": word,
        "exists": DICTIONARY.word_exists(word_clean),
        "definition": DICTIONARY.get_definition(word_clean),
        "lemmatization": LEMMATIZER.lemmatize(word_clean),
        "suggestions": []
    }
    
    # Si le mot n'existe pas, suggérer des corrections
    if not info["exists"]:
        spell_checker = SpellChecker(DICTIONARY.words)
        result = spell_checker.check_word(word_clean)
        info["suggestions"] = result.get("suggestions", [])
    
    return info


def format_suggestions_by_category(suggestions: List[Dict]) -> Dict:
    """
    Organise les suggestions par catégorie pour l'affichage
    """
    categorized = {
        "symbolic": [],
        "algorithmic": [],
        "structure": []
    }
    
    for sugg in suggestions:
        category = sugg.get("category", "algorithmic")
        categorized[category].append(sugg)
    
    return categorized


def get_text_quality_score(results: Dict) -> Dict:
    """
    Calcule un score de qualité du texte
    
    Args:
        results: Résultats de check_text_complete()
    
    Returns:
        Dict avec score et détails
    """
    stats = results["statistics"]
    
    # Critères de notation
    score = 100
    details = []
    
    # Pénalités

    errors = stats.get("errors", 0)
    warnings = stats.get("warnings", 0)
    
    # Erreurs graves : -10 points chacune
    score -= errors * 10
    if errors > 0:
        details.append(f"-{errors * 10} pts : {errors} erreur(s) grave(s)")
    
    # Avertissements : -5 points chacun
    score -= warnings * 5
    if warnings > 0:
        details.append(f"-{warnings * 5} pts : {warnings} avertissement(s)")
    
    # Bonus pour conformité VSO
    vso_compliance = stats.get("vso_compliance", 0)
    if vso_compliance >= 80:
        score += 5
        details.append("+5 pts : Bonne structure VSO")
    
    # S'assurer que le score reste entre 0 et 100
    score = max(0, min(100, score))
    
    # Déterminer le niveau
    if score >= 90:
        level = "Excellent"
    elif score >= 75:
        level = "Bon"
    elif score >= 60:
        level = "Moyen"
    elif score >= 40:
        level = "Passable"
    else:
        level = "À améliorer"
    
    return {
        "score": score,
        "level": level,
        "details": details
    }


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEST DE L'API COMPLÈTE D'ANALYSE MALAGASY")
    print("=" * 70)
    
    # Textes de test
    test_texts = [
        "Manao ahoana ianao androany?",
        "Mihinana sakafo aho amin'ny hariva.",
        "Tsaara daholo ny fianakaviana.",  # Erreur : tsaara → tsara
        "Le livre est nbien écrit.",       # Erreur : français + nb
        "Mandeha any an-tsena aho sy ny rahavaviko fa mila mividy vary.",
        "Nkomba vaovao"  # Erreur : nk en début
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'=' * 70}")
        print(f"TEST {i} : '{text}'")
        print('=' * 70)
        
        # Analyse complète
        results = check_text_complete(text)
        
        # Afficher les suggestions par catégorie
        categorized = format_suggestions_by_category(results["suggestions"])
        
        print("\n STATISTIQUES :")
        stats = results["statistics"]
        print(f"   - Mots totaux : {stats['total_words']}")
        print(f"   - Mots uniques : {stats['unique_words']}")
        print(f"   - Phrases : {stats['total_sentences']}")
        print(f"   - Longueur moyenne : {stats['average_sentence_length']:.1f} mots/phrase")
        print(f"   - Conformité VSO : {stats['vso_compliance']:.0f}%")
        
        # Score de qualité
        quality = get_text_quality_score(results)
        print(f"\n SCORE DE QUALITÉ : {quality['score']}/100 ({quality['level']})")
        if quality['details']:
            for detail in quality['details']:
                print(f"   {detail}")
        
        # Afficher les suggestions
        if results["suggestions"]:
            print(f"\n  SUGGESTIONS ({len(results['suggestions'])}) :")
            
            # Erreurs symboliques
            if categorized["symbolic"]:
                print(f"\n    Règles linguistiques ({len(categorized['symbolic'])}) :")
                for sugg in categorized["symbolic"][:3]:
                    print(f"      [{sugg['severity']}] {sugg['message']}")
                    print(f"      → {sugg['suggestion']}")
            
            # Erreurs algorithmiques
            if categorized["algorithmic"]:
                print(f"\n    Orthographe ({len(categorized['algorithmic'])}) :")
                for sugg in categorized["algorithmic"][:3]:
                    print(f"      [{sugg['severity']}] {sugg['message']}")
                    if 'alternatives' in sugg and sugg['alternatives']:
                        print(f"      → Suggestions : {', '.join(sugg['alternatives'][:3])}")
            
            # Erreurs de structure
            if categorized["structure"]:
                print(f"\n   🔵 Structure ({len(categorized['structure'])}) :")
                for sugg in categorized["structure"][:3]:
                    print(f"      [{sugg['severity']}] {sugg['message']}")
        else:
            print("\n Aucune suggestion - Texte correct !")
    
    # Test de l'autocomplétion
    print(f"\n\n{'=' * 70}")
    print("TEST AUTOCOMPLÉTION")
    print('=' * 70)
    
    prefixes = ["ma", "mi", "ts"]
    for prefix in prefixes:
        completions = autocomplete_word(prefix, top_k=5)
        print(f"\n'{prefix}...' → {', '.join(completions[:5])}")
    
    # Test d'info sur un mot
    print(f"\n\n{'=' * 70}")
    print("TEST INFO SUR UN MOT")
    print('=' * 70)
    
    test_word = "mihinana"
    info = get_word_info(test_word)
    print(f"\nMot : '{test_word}'")
    print(f"   - Existe : {'✓' if info['exists'] else '✗'}")
    print(f"   - Racine : {info['lemmatization']['root']}")
    print(f"   - Préfixe : {info['lemmatization']['prefix'] or '-'}")
    print(f"   - Suffixe : {info['lemmatization']['suffix'] or '-'}")
    
    print("\n" + "=" * 70)
    print(" TOUS LES TESTS TERMINÉS")
    print("=" * 70)