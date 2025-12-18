# api.py
"""
API FastAPI pour l'éditeur de texte Malagasy
Intègre tous les modules NLP (symbolic + algorithmic)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.nlp.nlp_checker import (
    check_text_complete,
    get_next_word_predictions,
    autocomplete_word,
    get_word_info,
    get_text_quality_score,
    format_suggestions_by_category
)
from backend.nlp.dictionary_loader import MalagasyDictionary
from backend.nlp.algorithmic import MalagasyLemmatizer, SentenceAnalyzer
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation FastAPI
app = FastAPI(
    title="API Éditeur Malagasy IA",
    description="API pour l'analyse et correction de textes en Malagasy",
    version="1.0.0"
)

# Configuration CORS pour React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger les modèles au démarrage
logger.info("🔄 Chargement des modèles NLP...")
DICTIONARY = MalagasyDictionary()
LEMMATIZER = MalagasyLemmatizer()
ANALYZER = SentenceAnalyzer()
logger.info("✅ Modèles chargés avec succès")


# ============================================================
# MODÈLES PYDANTIC (Validation des données)
# ============================================================

class TextInput(BaseModel):
    text: str

class WordInput(BaseModel):
    word: str

class ContextInput(BaseModel):
    context: List[str]
    limit: Optional[int] = 5

class TranslationInput(BaseModel):
    word: str
    direction: Optional[str] = "mg-fr"  # "mg-fr" ou "fr-mg"


# ============================================================
# ROUTES DE L'API
# ============================================================

@app.get("/")
async def home():
    """Page d'accueil de l'API"""
    return {
        "name": "API Éditeur Malagasy IA",
        "version": "1.0.0",
        "status": "running",
        "dictionary_size": len(DICTIONARY.words),
        "endpoints": {
            "check": "POST /api/check - Vérification complète du texte",
            "word_info": "POST /api/word-info - Informations sur un mot",
            "autocomplete": "GET /api/autocomplete?prefix=ma&limit=10",
            "predict": "POST /api/predict - Prédiction du mot suivant",
            "lemmatize": "POST /api/lemmatize - Lemmatisation",
            "sentiment": "POST /api/sentiment - Analyse de sentiment",
            "translate": "POST /api/translate - Traduction mot-à-mot",
            "stats": "GET /api/stats - Statistiques du dictionnaire"
        }
    }


@app.post("/api/check")
async def check_text(input_data: TextInput):
    """
    Vérification complète d'un texte
    
    Args:
        text: Texte à analyser
    
    Returns:
        Suggestions, analyses, statistiques, score de qualité
    """
    try:
        text = input_data.text
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide")
        
        # Analyse complète
        results = check_text_complete(text)
        
        # Ajouter le score de qualité
        quality_score = get_text_quality_score(results)
        results['quality_score'] = quality_score
        
        # Organiser les suggestions par catégorie
        categorized = format_suggestions_by_category(results['suggestions'])
        results['suggestions_by_category'] = categorized
        
        logger.info(f"✅ Texte analysé : {len(text)} caractères, {len(results['suggestions'])} suggestions")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/word-info")
async def word_info(input_data: WordInput):
    """
    Informations détaillées sur un mot
    
    Args:
        word: Mot à analyser
    
    Returns:
        Existence, définition, lemmatisation, suggestions
    """
    try:
        word = input_data.word.strip()
        
        if not word:
            raise HTTPException(status_code=400, detail="Le mot ne peut pas être vide")
        
        # Obtenir les infos
        info = get_word_info(word)
        
        return info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur word-info : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/autocomplete")
async def autocomplete(prefix: str, limit: int = 10):
    """
    Autocomplétion d'un préfixe
    
    Args:
        prefix: Début du mot (ex: "ma")
        limit: Nombre de suggestions (défaut: 10)
    
    Returns:
        Liste de complétions possibles
    """
    try:
        if not prefix:
            raise HTTPException(status_code=400, detail="Le paramètre 'prefix' est requis")
        
        if len(prefix) < 2:
            return {"prefix": prefix, "suggestions": [], "count": 0}
        
        # Obtenir les suggestions
        suggestions = autocomplete_word(prefix, top_k=limit)
        
        return {
            "prefix": prefix,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur autocomplete : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict")
async def predict_next(input_data: ContextInput):
    """
    Prédiction du mot suivant
    
    Args:
        context: Liste des mots précédents
        limit: Nombre de prédictions
    
    Returns:
        Liste de prédictions avec probabilités
    """
    try:
        context = input_data.context
        limit = input_data.limit
        
        if not context:
            raise HTTPException(status_code=400, detail="Le contexte ne peut pas être vide")
        
        # Obtenir les prédictions
        predictions = get_next_word_predictions(context, top_k=limit)
        
        return {
            "context": context,
            "predictions": predictions,
            "count": len(predictions)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur predict : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/lemmatize")
async def lemmatize(input_data: WordInput):
    """
    Lemmatisation d'un mot
    
    Args:
        word: Mot à lemmatiser
    
    Returns:
        Racine, préfixe, suffixe
    """
    try:
        word = input_data.word.strip()
        
        if not word:
            raise HTTPException(status_code=400, detail="Le mot ne peut pas être vide")
        
        # Lemmatiser
        result = LEMMATIZER.lemmatize(word)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lemmatize : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sentiment")
async def sentiment(input_data: TextInput):
    """
    Analyse de sentiment (simple)
    
    Args:
        text: Texte à analyser
    
    Returns:
        Sentiment positif/négatif/neutre
    """
    try:
        text = input_data.text.lower()
        
        # Mots positifs en malagasy
        positive_words = [
            "faly", "tsara", "mahafaly", "mendrika", "soa", "marina",
            "mahafinaritra", "mahagaga", "be", "lehibe", "misaotra",
            "fitiavana", "sambatra", "mazava", "malaza"
        ]
        
        # Mots négatifs en malagasy
        negative_words = [
            "malahelo", "ratsy", "mafy", "sarotra", "tsy", "marary",
            "sosotra", "diso", "mangetaheta", "mangidy", "mahantra",
            "kivy", "mampalahelo"
        ]
        
        # Compter
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Déterminer le sentiment
        total = positive_count + negative_count
        
        if total == 0:
            sentiment_result = "neutre"
            score = 0.5
        elif positive_count > negative_count:
            sentiment_result = "positif"
            score = positive_count / total
        elif negative_count > positive_count:
            sentiment_result = "négatif"
            score = negative_count / total
        else:
            sentiment_result = "neutre"
            score = 0.5
        
        # Emoji selon sentiment
        emoji = "😊" if sentiment_result == "positif" else "😢" if sentiment_result == "négatif" else "😐"
        
        return {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "sentiment": sentiment_result,
            "emoji": emoji,
            "score": round(score, 2),
            "positive_words": positive_count,
            "negative_words": negative_count,
            "confidence": "élevée" if abs(positive_count - negative_count) > 2 else "moyenne"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur sentiment : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate")
async def translate(input_data: TranslationInput):
    """
    Traduction mot-à-mot Malagasy <-> Français
    
    Args:
        word: Mot à traduire
        direction: "mg-fr" ou "fr-mg"
    
    Returns:
        Traduction du mot
    """
    try:
        word = input_data.word.strip().lower()
        direction = input_data.direction
        
        # Dictionnaire de traduction étendu
        translations_mg_fr = {
            # Verbes
            "manao": "faire",
            "mihinana": "manger",
            "misotro": "boire",
            "mandeha": "aller/partir",
            "matory": "dormir",
            "mifoha": "se réveiller",
            "miasa": "travailler",
            "mianatra": "étudier",
            "miteny": "parler",
            "mamaky": "lire",
            "manoratra": "écrire",
            "mijery": "regarder",
            "mihaino": "écouter",
            "manome": "donner",
            "mandray": "recevoir",
            
            # Pronoms
            "aho": "je/moi",
            "ianao": "tu/toi",
            "izy": "il/elle",
            "isika": "nous (inclusif)",
            "izahay": "nous (exclusif)",
            "ianareo": "vous",
            
            # Adjectifs
            "tsara": "bon/bien",
            "ratsy": "mauvais",
            "faly": "heureux/content",
            "lehibe": "grand",
            "kely": "petit",
            "lava": "long",
            "fohy": "court",
            "mafana": "chaud",
            "mangatsiaka": "froid",
            
            # Noms
            "trano": "maison",
            "sakafo": "nourriture",
            "rano": "eau",
            "vary": "riz",
            "hena": "viande",
            "mofo": "pain",
            "boky": "livre",
            "tany": "terre/pays",
            "lanitra": "ciel",
            "masoandro": "soleil",
            "volana": "lune/mois",
            
            # Temps
            "omaly": "hier",
            "androany": "aujourd'hui",
            "rahampitso": "demain",
            "maraina": "matin",
            "hariva": "soir",
            "alina": "nuit",
            
            # Autres
            "tsy": "ne...pas",
            "eny": "oui",
            "tsia": "non",
            "misaotra": "merci",
            "azafady": "s'il vous plaît/excusez-moi",
            "veloma": "au revoir"
        }
        
        if direction == "mg-fr":
            translation = translations_mg_fr.get(word, None)
        else:
            # Inverser le dictionnaire
            translations_fr_mg = {v: k for k, v in translations_mg_fr.items()}
            translation = translations_fr_mg.get(word, None)
        
        if translation is None:
            return {
                "word": word,
                "translation": None,
                "direction": direction,
                "found": False,
                "message": "Traduction non disponible dans le dictionnaire"
            }
        
        return {
            "word": word,
            "translation": translation,
            "direction": direction,
            "found": True
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur translate : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def stats():
    """
    Statistiques du dictionnaire et de l'API
    
    Returns:
        Nombre de mots, couverture, etc.
    """
    try:
        dict_stats = DICTIONARY.get_statistics()
        
        return {
            "dictionary": dict_stats,
            "api": {
                "status": "operational",
                "version": "1.0.0"
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur stats : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "dictionary_loaded": len(DICTIONARY.words) > 0
    }


# ============================================================
# DÉMARRAGE DU SERVEUR
# ============================================================

# if __name__ == '__main__':
#     import uvicorn
    
#     print("=" * 70)
#     print("🚀 DÉMARRAGE DE L'API ÉDITEUR MALAGASY IA (FastAPI)")
#     print("=" * 70)
#     print(f"📚 Dictionnaire : {len(DICTIONARY.words)} mots")
#     print(f"🌐 URL API : http://localhost:8000")
#     print(f"📖 Documentation interactive : http://localhost:8000/docs")
#     print(f"📋 Documentation alternative : http://localhost:8000/redoc")
#     print("=" * 70)
    
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)