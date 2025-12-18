# scraper_tools.py
"""
Scripts de scraping pour enrichir le dictionnaire Malagasy
Sources : Wikipedia MG, Teny Malagasy, Bible, etc.
VERSION CORRIGÉE
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from pathlib import Path
from collections import Counter

# ============================================================
# 1. SCRAPER WIKIPEDIA MALAGASY (VERSION CORRIGÉE)
# ============================================================

def scrape_wikipedia_mg(num_pages=100, save_to_file=True):
    """
    Scrape des articles aléatoires de Wikipedia Malagasy.
    Retourne un ensemble de mots uniques.
    """
    print(f"🔍 Scraping Wikipedia Malagasy ({num_pages} pages)...")
    
    words = set()
    api_url = "https://mg.wikipedia.org/w/api.php"
    
    # Paramètres pour obtenir des pages aléatoires
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": "0",
        "rnlimit": min(num_pages, 10)  # Réduire à 10 par batch
    }
    
    try:
        # Ajouter un user-agent
        headers = {
            'User-Agent': 'MalagasyDictionaryBot/1.0 (Educational Project)'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        
        # Debug
        print(f"   Status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return set()
        
        data = response.json()
        
        if "query" in data and "random" in data["query"]:
            pages = data["query"]["random"]
            print(f"   ✓ {len(pages)} pages récupérées")
            
            for page in pages:
                page_title = page.get("title", "")
                
                # Extraire les mots du titre directement
                title_words = extract_malagasy_words(page_title)
                words.update(title_words)
                
                # Optionnel : récupérer le contenu (plus lent)
                try:
                    page_id = page["id"]
                    content_params = {
                        "action": "query",
                        "format": "json",
                        "pageids": page_id,
                        "prop": "extracts",
                        "explaintext": True,
                        "exintro": True  # Seulement l'introduction
                    }
                    
                    content_response = requests.get(api_url, params=content_params, 
                                                   headers=headers, timeout=10)
                    content_data = content_response.json()
                    
                    if "query" in content_data and "pages" in content_data["query"]:
                        page_data = content_data["query"]["pages"].get(str(page_id), {})
                        extract = page_data.get("extract", "")
                        
                        if extract:
                            page_words = extract_malagasy_words(extract)
                            words.update(page_words)
                            print(f"      ✓ {page_title[:30]}... : +{len(page_words)} mots")
                    
                    time.sleep(0.3)
                    
                except Exception as e:
                    print(f"      ⚠️  Contenu inaccessible pour {page_title}")
                    continue
        
        print(f"\n✅ Scraping terminé : {len(words)} mots uniques extraits")
        
        if save_to_file and words:
            save_words_to_file(words, "data/wikipedia_words.txt")
        
        return words
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau : {e}")
        return set()
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON : {e}")
        print(f"   Réponse brute : {response.text[:200]}")
        return set()
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return set()


# ============================================================
# 2. SCRAPER WIKIPEDIA PAR RECHERCHE (VERSION CORRIGÉE)
# ============================================================

def scrape_wikipedia_by_search(search_terms=None):
    """
    Scrape Wikipedia MG en cherchant des termes spécifiques
    """
    if search_terms is None:
        search_terms = [
            "Madagasikara", "Antananarivo", "sakafo", "fihavanana",
            "fomba", "tantara", "fambolena", "biby", "hazo", "fanabeazana"
        ]
    
    print(f"🔍 Scraping Wikipedia par recherche ({len(search_terms)} thèmes)...")
    
    words = set()
    api_url = "https://mg.wikipedia.org/w/api.php"
    
    headers = {
        'User-Agent': 'MalagasyDictionaryBot/1.0 (Educational Project)'
    }
    
    for term in search_terms:
        try:
            # Rechercher le terme
            search_params = {
                "action": "opensearch",
                "format": "json",
                "search": term,
                "limit": 5
            }
            
            response = requests.get(api_url, params=search_params, 
                                  headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"   ✗ '{term}': Erreur HTTP {response.status_code}")
                continue
            
            data = response.json()
            
            # Format OpenSearch : [query, [titles], [descriptions], [urls]]
            if len(data) >= 2 and data[1]:
                titles = data[1]
                
                for title in titles[:3]:  # Prendre les 3 premiers résultats
                    # Extraire mots du titre
                    title_words = extract_malagasy_words(title)
                    words.update(title_words)
                
                print(f"   ✓ '{term}': {len(titles)} résultats, +{len(title_words)} mots")
            else:
                print(f"   ⚠️  '{term}': Aucun résultat")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ✗ '{term}': {str(e)}")
            continue
    
    print(f"\n✅ Scraping terminé : {len(words)} mots uniques")
    
    if words:
        save_words_to_file(words, "data/wikipedia_search_words.txt")
    
    return words


# ============================================================
# 3. SCRAPER SIMPLE : PAGES WIKIPEDIA DIRECTES
# ============================================================

def scrape_wikipedia_direct():
    """
    Méthode alternative : scraper directement des pages HTML Wikipedia
    Plus fiable que l'API
    """
    print("🔍 Scraping direct de pages Wikipedia...")
    
    words = set()
    
    # Liste de pages importantes en Malagasy
    pages = [
        "Madagasikara",
        "Antananarivo",
        "Fianarantsoa",
        "Toamasina",
        "Mahajanga",
        "Toliara",
        "Ranomasina_Indianina",
        "Fambolena",
        "Kolontsaina_malagasy"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for page in pages:
        try:
            url = f"https://mg.wikipedia.org/wiki/{page}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraire le contenu principal
                content = soup.find('div', {'id': 'mw-content-text'})
                
                if content:
                    # Supprimer les éléments indésirables
                    for tag in content.find_all(['script', 'style', 'sup', 'table']):
                        tag.decompose()
                    
                    text = content.get_text()
                    page_words = extract_malagasy_words(text)
                    words.update(page_words)
                    
                    print(f"   ✓ {page}: +{len(page_words)} mots")
                else:
                    print(f"   ⚠️  {page}: Contenu non trouvé")
            else:
                print(f"   ✗ {page}: HTTP {response.status_code}")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"   ✗ {page}: {str(e)}")
            continue
    
    print(f"\n✅ Scraping terminé : {len(words)} mots uniques")
    
    if words:
        save_words_to_file(words, "data/wikipedia_direct_words.txt")
    
    return words


# ============================================================
# 4. SCRAPER BIBLE MALAGASY (VERSION SIMPLIFIÉE)
# ============================================================

def scrape_bible_malagasy():
    """
    Scrape la Bible en Malagasy depuis Wikisource
    """
    print("🔍 Scraping Bible Malagasy...")
    
    words = set()
    
    # URLs de quelques livres de la Bible sur Wikisource
    bible_pages = [
        "https://mg.wikisource.org/wiki/Genesisy",
        "https://mg.wikisource.org/wiki/Eksodosy",
        "https://mg.wikisource.org/wiki/Salamo"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in bible_pages:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraire le texte
                content = soup.find('div', {'class': 'mw-parser-output'})
                
                if content:
                    text = content.get_text()
                    page_words = extract_malagasy_words(text)
                    words.update(page_words)
                    
                    book_name = url.split('/')[-1]
                    print(f"   ✓ {book_name}: +{len(page_words)} mots")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"   ✗ Erreur : {str(e)}")
            continue
    
    print(f"\n✅ {len(words)} mots extraits de la Bible")
    
    if words:
        save_words_to_file(words, "data/bible_words.txt")
    
    return words


# ============================================================
# 5. UTILITAIRES (CORRIGÉS)
# ============================================================

def extract_malagasy_words(text):
    """
    Extrait uniquement les mots malagasy valides d'un texte.
    """
    if not text:
        return set()
    
    # Nettoyer le texte
    text = text.lower()
    
    # Supprimer les caractères non-malagasy et ponctuation
    text = re.sub(r'[^abdefghijklmnoprstvy\s\']', ' ', text)
    
    # Supprimer les apostrophes isolées
    text = re.sub(r'\s+\'|\'\s+', ' ', text)
    
    # Extraire les mots
    words = text.split()
    
    # Filtrer
    valid_words = set()
    for word in words:
        word = word.strip("'")
        
        # Conditions de validation
        if (2 <= len(word) <= 20 and  # Entre 2 et 20 lettres
            not word.isdigit() and  # Pas un nombre
            word.isalpha()):  # Que des lettres
            
            valid_words.add(word)
    
    return valid_words


def save_words_to_file(words, filepath):
    """Sauvegarde une liste de mots dans un fichier texte"""
    if not words:
        print(f"⚠️  Aucun mot à sauvegarder")
        return
    
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for word in sorted(words):
            f.write(f"{word}\n")
    
    print(f"💾 {len(words)} mots sauvegardés dans : {filepath}")


def merge_dictionaries():
    """
    Fusionne tous les dictionnaires dans un seul fichier
    """
    print("🔄 Fusion des dictionnaires...")
    
    all_words = set()
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("❌ Dossier 'data/' introuvable")
        return set()
    
    # Charger tous les fichiers de mots
    word_files = [
        "malagasy_words.txt",
        "wikipedia_words.txt",
        "wikipedia_search_words.txt",
        "wikipedia_direct_words.txt",
        "bible_words.txt"
    ]
    
    for filename in word_files:
        filepath = data_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    words = [line.strip().lower() for line in f 
                            if line.strip() and not line.startswith('#')]
                    all_words.update(words)
                    print(f"   ✓ {filename}: {len(words)} mots")
            except Exception as e:
                print(f"   ✗ {filename}: {str(e)}")
    
    if all_words:
        # Sauvegarder le dictionnaire fusionné
        merged_file = data_dir / "malagasy_complete.txt"
        save_words_to_file(all_words, merged_file)
        
        print(f"\n✅ Dictionnaire complet : {len(all_words)} mots uniques")
    else:
        print("\n⚠️  Aucun mot trouvé à fusionner")
    
    return all_words


# ============================================================
# SCRIPT PRINCIPAL
# ============================================================

def main():
    """
    Script principal pour enrichir le dictionnaire
    """
    print("=" * 70)
    print("ENRICHISSEMENT DU DICTIONNAIRE MALAGASY")
    print("=" * 70)
    
    print("\n📋 Choisissez une option :")
    print("   1. Scraper Wikipedia MG (pages aléatoires) - API")
    print("   2. Scraper Wikipedia MG (par recherche) - API")
    print("   3. Scraper Wikipedia MG (direct) - HTML ⭐ RECOMMANDÉ")
    print("   4. Scraper Bible Malagasy")
    print("   5. Tout scraper (3+4)")
    print("   6. Fusionner tous les dictionnaires")
    
    choice = input("\n👉 Votre choix (1-6) : ").strip()
    
    if choice == "1":
        scrape_wikipedia_mg(num_pages=20)
    
    elif choice == "2":
        scrape_wikipedia_by_search()
    
    elif choice == "3":
        scrape_wikipedia_direct()
    
    elif choice == "4":
        scrape_bible_malagasy()
    
    elif choice == "5":
        print("\n🚀 Scraping complet lancé...\n")
        scrape_wikipedia_direct()
        print("\n" + "-" * 70 + "\n")
        scrape_bible_malagasy()
        print("\n" + "-" * 70 + "\n")
        merge_dictionaries()
    
    elif choice == "6":
        merge_dictionaries()
    
    else:
        print("❌ Choix invalide")
    
    print("\n" + "=" * 70)
    print("✅ TERMINÉ !")
    print("=" * 70)


if __name__ == "__main__":
    main()