# nlp/algorithmic.py
"""
Module algorithmique pour l'analyse avancée du texte Malagasy.
Inclut : Levenshtein, N-grams, lemmatisation, autocomplétion, analyse de phrases.
"""

from rapidfuzz import fuzz, process
from collections import Counter, defaultdict
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set

# ============================================================
# 1. CORRECTION ORTHOGRAPHIQUE (LEVENSHTEIN)
# ============================================================

class SpellChecker:
    """
    Correcteur orthographique basé sur la distance de Levenshtein
    """
    
    def __init__(self, dictionary_words: Set[str]):
        self.dictionary = dictionary_words
    
    def check_word(self, word: str, threshold: int = 70) -> Dict:
        """
        Vérifie un mot et retourne des suggestions si incorrect
        
        Args:
            word: Le mot à vérifier
            threshold: Score minimum de similarité (0-100)
        
        Returns:
            Dict avec statut et suggestions
        """
        word_clean = word.lower().strip(".,!?;:\"'")
        
        if word_clean in self.dictionary:
            return {
                "correct": True,
                "word": word,
                "suggestions": []
            }
        
        # Trouver les mots similaires
        matches = process.extract(
            word_clean,
            self.dictionary,
            scorer=fuzz.ratio,
            limit=5
        )
        
        # Filtrer par seuil
        suggestions = [match[0] for match in matches if match[1] >= threshold]
        
        return {
            "correct": False,
            "word": word,
            "suggestions": suggestions,
            "best_match": suggestions[0] if suggestions else None,
            "confidence": matches[0][1] if matches else 0
        }
    
    def correct_text(self, text: str, auto_correct: bool = False) -> List[Dict]:
        """
        Corrige un texte entier
        """
        words = text.split()
        corrections = []
        
        for i, word in enumerate(words):
            result = self.check_word(word)
            
            if not result["correct"]:
                correction = {
                    "position": text.find(word),
                    "original": word,
                    "suggestions": result["suggestions"],
                    "type": "spelling"
                }
                
                if auto_correct and result["best_match"]:
                    correction["corrected"] = result["best_match"]
                
                corrections.append(correction)
        
        return corrections


# ============================================================
# 2. LEMMATISATION (Extraction de racines)
# ============================================================

class MalagasyLemmatizer:
    """
    Lemmatiseur pour retrouver la racine des mots malagasy
    """
    
    def __init__(self):
        # Préfixes malagasy courants
        self.prefixes = [
            "maha", "mpam", "mpan", "fam", "fan", "mam", "man", "mpa", 
            "ma", "mi", "fi", "mp", "f", "m", "tsy"
        ]
        
        # Suffixes malagasy courants
        self.suffixes = [
            "nana", "itra", "ana", "ina", "na", "tra", "ka", "ny"
        ]
        
        # Ordre : plus long en premier pour éviter les faux positifs
        self.prefixes.sort(key=len, reverse=True)
        self.suffixes.sort(key=len, reverse=True)
    
    def lemmatize(self, word: str) -> Dict:
        """
        Retrouve la racine d'un mot
        
        Returns:
            Dict avec racine, préfixe, suffixe
        """
        word = word.lower().strip()
        original = word
        
        prefix_found = ""
        suffix_found = ""
        
        # Retirer le préfixe
        for prefix in self.prefixes:
            if word.startswith(prefix) and len(word) > len(prefix) + 2:
                prefix_found = prefix
                word = word[len(prefix):]
                break
        
        # Retirer le suffixe
        for suffix in self.suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                suffix_found = suffix
                word = word[:-len(suffix)]
                break
        
        return {
            "original": original,
            "root": word,
            "prefix": prefix_found,
            "suffix": suffix_found,
            "has_prefix": bool(prefix_found),
            "has_suffix": bool(suffix_found)
        }
    
    def lemmatize_text(self, text: str) -> List[Dict]:
        """
        Lemmatise tous les mots d'un texte
        """
        words = text.split()
        results = []
        
        for word in words:
            word_clean = word.strip(".,!?;:\"'")
            if word_clean:
                result = self.lemmatize(word_clean)
                results.append(result)
        
        return results


# ============================================================
# 3. N-GRAMS ET AUTOCOMPLÉTION
# ============================================================

class NGramModel:
    """
    Modèle N-gram pour la prédiction de mots et l'autocomplétion
    """
    
    def __init__(self, n: int = 2):
        self.n = n
        self.ngrams = defaultdict(Counter)
        self.word_freq = Counter()
    
    def train(self, texts: List[str]):
        """
        Entraîne le modèle sur un corpus de textes
        
        Args:
            texts: Liste de phrases en malagasy
        """
        for text in texts:
            words = text.lower().split()
            
            # Compter la fréquence des mots
            self.word_freq.update(words)
            
            # Créer les n-grams
            for i in range(len(words) - self.n + 1):
                # Contexte = n-1 premiers mots
                context = tuple(words[i:i+self.n-1])
                # Mot suivant
                next_word = words[i+self.n-1]
                self.ngrams[context][next_word] += 1
    
    def predict_next_word(self, context: List[str], top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Prédit les k mots les plus probables après un contexte
        
        Args:
            context: Liste des mots précédents
            top_k: Nombre de prédictions à retourner
        
        Returns:
            Liste de tuples (mot, probabilité)
        """
        # Prendre les n-1 derniers mots comme contexte
        context = tuple(context[-(self.n-1):])
        
        if context not in self.ngrams:
            # Fallback : retourner les mots les plus fréquents
            return [(word, freq) for word, freq in self.word_freq.most_common(top_k)]
        
        # Calculer les probabilités
        candidates = self.ngrams[context]
        total = sum(candidates.values())
        
        predictions = [
            (word, count / total) 
            for word, count in candidates.most_common(top_k)
        ]
        
        return predictions
    
    def autocomplete(self, prefix: str, top_k: int = 5) -> List[str]:
        """
        Suggère des complétions pour un préfixe
        
        Args:
            prefix: Début du mot à compléter
            top_k: Nombre de suggestions
        
        Returns:
            Liste de mots possibles
        """
        prefix = prefix.lower()
        
        # Trouver tous les mots qui commencent par ce préfixe
        candidates = [
            word for word in self.word_freq.keys() 
            if word.startswith(prefix)
        ]
        
        # Trier par fréquence
        candidates.sort(key=lambda w: self.word_freq[w], reverse=True)
        
        return candidates[:top_k]
    
    def save_model(self, filepath: str):
        """Sauvegarde le modèle"""
        data = {
            "n": self.n,
            "ngrams": {str(k): dict(v) for k, v in self.ngrams.items()},
            "word_freq": dict(self.word_freq)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_model(self, filepath: str):
        """Charge un modèle sauvegardé"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.n = data["n"]
        self.word_freq = Counter(data["word_freq"])
        
        # Reconvertir les clés en tuples
        self.ngrams = defaultdict(Counter)
        for k, v in data["ngrams"].items():
            key = eval(k)  # Convertir string en tuple
            self.ngrams[key] = Counter(v)


# ============================================================
# 4. ANALYSE DE PHRASES
# ============================================================

class SentenceAnalyzer:
    """
    Analyseur de phrases en Malagasy
    """
    
    def __init__(self):
        # Ordre des mots : VSO (Verbe-Sujet-Objet)
        self.verb_prefixes = ["mi", "ma", "man", "mam", "maha", "mpan", "mpam", "m"]
        
        # Mots de liaison
        self.conjunctions = ["sy", "ary", "fa", "kanefa", "nefa", "satria", "raha", "na"]
        
        # Prépositions
        self.prepositions = ["amin'ny", "amin", "eo", "any", "aty", "avy", "ho", "ao"]
    
    def analyze_sentence(self, sentence: str) -> Dict:
        """
        Analyse une phrase malagasy
        
        Returns:
            Dict avec structure, type, complexité
        """
        words = sentence.strip().split()
        
        if not words:
            return {"error": "Phrase vide"}
        
        analysis = {
            "sentence": sentence,
            "word_count": len(words),
            "has_verb": False,
            "verb_position": None,
            "has_conjunction": False,
            "conjunctions_found": [],
            "has_preposition": False,
            "prepositions_found": [],
            "structure_type": "simple",
            "vso_order": False
        }
        
        # Détecter les verbes
        for i, word in enumerate(words):
            word_lower = word.lower()
            
            # Vérifier si c'est un verbe
            for prefix in self.verb_prefixes:
                if word_lower.startswith(prefix) and len(word_lower) > len(prefix) + 1:
                    analysis["has_verb"] = True
                    if analysis["verb_position"] is None:
                        analysis["verb_position"] = i
                    break
            
            # Vérifier conjonctions
            if word_lower in self.conjunctions:
                analysis["has_conjunction"] = True
                analysis["conjunctions_found"].append(word_lower)
            
            # Vérifier prépositions
            if word_lower in self.prepositions:
                analysis["has_preposition"] = True
                analysis["prepositions_found"].append(word_lower)
        
        # Analyser l'ordre VSO
        if analysis["has_verb"] and analysis["verb_position"] == 0:
            analysis["vso_order"] = True
        
        # Déterminer le type de structure
        if analysis["has_conjunction"]:
            analysis["structure_type"] = "complexe"
        elif analysis["word_count"] > 10:
            analysis["structure_type"] = "composée"
        
        return analysis
    
    def split_sentences(self, text: str) -> List[str]:
        """
        Sépare un texte en phrases
        """
        # Séparateurs de phrases en malagasy
        # Utilise . ! ? et aussi les retours à la ligne
        sentences = re.split(r'[.!?]+', text)
        
        # Nettoyer et filtrer
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyse un texte complet (plusieurs phrases)
        """
        sentences = self.split_sentences(text)
        
        analysis = {
            "text": text,
            "sentence_count": len(sentences),
            "sentences": [],
            "average_words": 0,
            "vso_percentage": 0,
            "complex_sentences": 0
        }
        
        total_words = 0
        vso_count = 0
        
        for sentence in sentences:
            sent_analysis = self.analyze_sentence(sentence)
            analysis["sentences"].append(sent_analysis)
            
            total_words += sent_analysis["word_count"]
            
            if sent_analysis.get("vso_order"):
                vso_count += 1
            
            if sent_analysis.get("structure_type") in ["complexe", "composée"]:
                analysis["complex_sentences"] += 1
        
        # Calculer les statistiques
        if sentences:
            analysis["average_words"] = total_words / len(sentences)
            analysis["vso_percentage"] = (vso_count / len(sentences)) * 100
        
        return analysis


# ============================================================
# 5. VALIDATEUR DE PHRASES
# ============================================================

class SentenceValidator:
    """
    Valide la structure des phrases malagasy
    """
    
    def __init__(self):
        self.analyzer = SentenceAnalyzer()
    
    def validate_sentence(self, sentence: str) -> List[Dict]:
        """
        Valide une phrase et retourne des suggestions
        """
        suggestions = []
        
        analysis = self.analyzer.analyze_sentence(sentence)
        words = sentence.split()
        
        # Règle 1 : Phrase trop courte
        if analysis["word_count"] < 2:
            suggestions.append({
                "type": "structure",
                "severity": "info",
                "message": "Phrase très courte",
                "suggestion": "Une phrase complète contient généralement au moins un verbe et un sujet"
            })
        
        # Règle 2 : Pas de verbe détecté
        if not analysis["has_verb"] and analysis["word_count"] > 3:
            suggestions.append({
                "type": "structure",
                "severity": "warning",
                "message": "Aucun verbe détecté dans cette phrase",
                "suggestion": "Une phrase malagasy commence généralement par un verbe (ordre VSO)"
            })
        
        # Règle 3 : Verbe pas en première position
        if analysis["has_verb"] and not analysis["vso_order"] and analysis["word_count"] > 4:
            suggestions.append({
                "type": "syntaxe",
                "severity": "info",
                "message": "Le verbe n'est pas en première position",
                "suggestion": "En Malagasy, l'ordre standard est VSO (Verbe-Sujet-Objet)"
            })
        
        # Règle 4 : Phrase trop longue sans ponctuation
        if analysis["word_count"] > 20 and not analysis["has_conjunction"]:
            suggestions.append({
                "type": "structure",
                "severity": "warning",
                "message": "Phrase très longue sans conjonction",
                "suggestion": "Envisagez de diviser en plusieurs phrases ou d'utiliser des conjonctions"
            })
        
        return suggestions


# ============================================================
# 6. FONCTION PRINCIPALE D'ANALYSE ALGORITHMIQUE
# ============================================================

def algorithmic_check(text: str, dictionary_words: Set[str] = None) -> Dict:
    """
    Fonction principale qui combine toutes les analyses algorithmiques
    
    Args:
        text: Texte à analyser
        dictionary_words: Ensemble de mots du dictionnaire
    
    Returns:
        Dict avec toutes les analyses
    """
    results = {
        "text": text,
        "spelling_errors": [],
        "lemmatization": [],
        "sentence_analysis": {},
        "sentence_validation": [],
        "statistics": {}
    }
    
    # 1. Correction orthographique
    if dictionary_words:
        spell_checker = SpellChecker(dictionary_words)
        results["spelling_errors"] = spell_checker.correct_text(text)
    
    # 2. Lemmatisation
    lemmatizer = MalagasyLemmatizer()
    results["lemmatization"] = lemmatizer.lemmatize_text(text)
    
    # 3. Analyse de phrases
    analyzer = SentenceAnalyzer()
    results["sentence_analysis"] = analyzer.analyze_text(text)
    
    # 4. Validation de phrases
    validator = SentenceValidator()
    sentences = analyzer.split_sentences(text)
    
    for sentence in sentences:
        validation = validator.validate_sentence(sentence)
        if validation:
            results["sentence_validation"].extend(validation)
    
    # 5. Statistiques
    words = text.split()
    results["statistics"] = {
        "total_words": len(words),
        "unique_words": len(set(w.lower() for w in words)),
        "total_sentences": len(sentences),
        "avg_sentence_length": results["sentence_analysis"].get("average_words", 0),
        "vso_compliance": results["sentence_analysis"].get("vso_percentage", 0)
    }
    
    return results


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEST DU MODULE ALGORITHMIQUE MALAGASY")
    print("=" * 70)
    
    # Textes de test
    test_texts = [
        "Manao ahoana ianao androany?",
        "Mihinana sakafo aho amin'ny hariva.",
        "Tsara ny toetr'andro fa mafana loatra.",
        "Mandeha any an-tsena aho sy ny rahavaviko.",
        "Tsy mahafantatra ny valiny aho satria sarotra ny fanontaniana."
    ]
    
    # Test 1 : Lemmatisation
    print("\n TEST 1 : LEMMATISATION")
    print("-" * 70)
    lemmatizer = MalagasyLemmatizer()
    
    test_words = ["mihinana", "mandeha", "mahafantatra", "fanomezana", "mamakiana"]
    for word in test_words:
        result = lemmatizer.lemmatize(word)
        print(f"   {word:15} → racine: {result['root']:10} "
              f"(préfixe: {result['prefix'] or '-':6}, suffixe: {result['suffix'] or '-'})")
    
    # Test 2 : Analyse de phrases
    print("\n TEST 2 : ANALYSE DE PHRASES")
    print("-" * 70)
    analyzer = SentenceAnalyzer()
    
    for text in test_texts:
        analysis = analyzer.analyze_sentence(text)
        print(f"\n   Phrase: '{text}'")
        print(f"      - Mots: {analysis['word_count']}")
        print(f"      - Verbe: {'✓' if analysis['has_verb'] else '✗'} "
              f"(position: {analysis['verb_position']})")
        print(f"      - VSO: {'✓' if analysis['vso_order'] else '✗'}")
        print(f"      - Type: {analysis['structure_type']}")
    
    # Test 3 : Validation
    print("\n TEST 3 : VALIDATION DE PHRASES")
    print("-" * 70)
    validator = SentenceValidator()
    
    for text in test_texts:
        suggestions = validator.validate_sentence(text)
        print(f"\n   Phrase: '{text}'")
        if suggestions:
            for sugg in suggestions:
                print(f"      [{sugg['severity']}] {sugg['message']}")
        else:
            print(f"      ✓ Aucun problème détecté")
    
    # Test 4 : N-grams (nécessite un corpus)
    print("\n TEST 4 : N-GRAMS ET PRÉDICTION")
    print("-" * 70)
    
    ngram_model = NGramModel(n=2)
    
    # Entraîner sur les textes de test
    training_corpus = [
        "manao ahoana ianao",
        "manao ahoana hianao",
        "mihinana sakafo aho",
        "misotro rano aho",
        "mandeha any an-tsena aho"
    ]
    
    ngram_model.train(training_corpus)
    
    # Tester la prédiction
    context = ["manao"]
    predictions = ngram_model.predict_next_word(context, top_k=3)
    print(f"\n   Après '{' '.join(context)}', les mots probables sont:")
    for word, prob in predictions:
        print(f"      - {word}: {prob:.2%}")
    
    # Tester l'autocomplétion
    prefix = "ma"
    completions = ngram_model.autocomplete(prefix, top_k=5)
    print(f"\n   Complétions pour '{prefix}':")
    for word in completions:
        print(f"      - {word}")
    
    print("\n" + "=" * 70)
    print(" TESTS TERMINÉS")
    print("=" * 70)