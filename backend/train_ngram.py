# train_ngram.py
"""
Script pour entraîner le modèle N-gram sur un corpus de phrases malagasy
"""

from nlp.algorithmic import NGramModel
from pathlib import Path

# ============================================================
# CORPUS DE PHRASES MALAGASY
# ============================================================

CORPUS_MALAGASY = [
    # Salutations et politesse
    "manao ahoana ianao",
    "manao ahoana hianao",
    "salama e",
    "veloma e",
    "misaotra betsaka",
    "azafady tompoko",
    "tsy misy fisaorana",
    "miala tsiny aho",
    
    # Vie quotidienne
    "mihinana sakafo aho",
    "misotro rano aho",
    "misotro kafe aho",
    "misotro dite aho",
    "matory aho ankehitriny",
    "mifoha maraina aho",
    "miasa aho isan'andro",
    "mianatra aho any amin'ny sekoly",
    
    # Famille
    "manao ahoana ny ray aman-dreninao",
    "tsara daholo ny fianakaviana",
    "misy zanaka efatra aho",
    "zoky lehibe aho amin'ny fianakaviana",
    "tiako ny rahavaviko",
    "manaja ny ray aman-dreny aho",
    
    # Déplacements
    "mandeha any an-tsena aho",
    "mandeha any am-piasana aho",
    "mandeha any an-tsekoly ny zanaka",
    "miverina any an-trano aho",
    "mitsidika ny havana aho",
    "mandeha amin'ny fiara aho",
    "mandeha an-tongotra aho",
    
    # Temps et météo
    "tsara ny toetr'andro androany",
    "mafana loatra ny andro",
    "mangatsiaka ny rivotra",
    "milatsaka ny orana",
    "mamirapiratra ny masoandro",
    "maizina ny lanitra",
    
    # Nourriture
    "tiako ny vary amin'ny hena",
    "matsiro ny sakafo",
    "noana aho izao",
    "mividy sakafo aho",
    "mahandro sakafo ny reniko",
    "mihinana vary sy laoka izahay",
    
    # Sentiments et états
    "faly aho androany",
    "malahelo aho",
    "sosotra loatra aho",
    "reraka aho izao",
    "salama tsara aho",
    "marary aho",
    "mangetaheta aho",
    
    # Travail et études
    "miasa mafy aho",
    "manoratra taratasy aho",
    "mamaky boky aho",
    "mianatra lesona aho",
    "manao devoara aho",
    "mijery fahitalavitra aho",
    
    # Questions courantes
    "aiza ianao izao",
    "aiza ny trano fivarotana",
    "firy ny vidiny",
    "oviana ianao hiverina",
    "iza no nankaty",
    "inona no vaovao",
    "nahoana ianao",
    
    # Actions quotidiennes
    "manasa lamba aho",
    "manadio trano aho",
    "mividy entana aho",
    "mandray vahiny aho",
    "manao lalao ny ankizy",
    "mihira aho",
    "mandihy aho",
    
    # Nature et environnement
    "tsara tarehy ny voninkazo",
    "avo ny tendrombohitra",
    "lalina ny ranomasina",
    "maitso ny hazo",
    "be ny biby any an'ala",
    
    # Phrases composées
    "mandeha any an-tsena aho fa mila mividy vary",
    "tsy afaka ho avy aho satria marary",
    "faly aho rehefa miverina ny raiko",
    "mihinana sakafo aho alohan'ny handehanako",
    "mamaky boky aho rehefa vita ny asa",
    
    # Négations
    "tsy mandeha aho androany",
    "tsy mahay miteny frantsay aho",
    "tsy tiako ny vary",
    "tsy faly aho",
    "tsy misy olona eto",
    "tsy ampy ny vola",
    
    # Capacités
    "mahay miteny malagasy aho",
    "mahay manoratra aho",
    "mahay mamaky aho",
    "mahay manao sakafo aho",
    "mahafantatra ny lalana aho",
    "mahalala ny vaovao aho",
    
    # Directions
    "any avaratra ny trano",
    "any atsimo ny ranomasina",
    "any atsinanana ny masoandro miposaka",
    "any andrefana ny masoandro milentika",
    "any ankavanana ny trano fivarotana",
    "any ankavia ny sekoly",
    
    # Couleurs et descriptions
    "fotsy ny kapoaka",
    "mainty ny lamba",
    "mena ny boky",
    "manga ny lanitra",
    "maitso ny ahitra",
    "mavo ny hazo",
    
    # Nombres et quantités
    "misy olona iray eto",
    "misy zanaka roa aho",
    "misy boky telo eo ambony latabatra",
    "mila efatra no ilaina",
    "vita dimy minitra",
    
    # Temps (chronologie)
    "omaly aho nandeha",
    "androany aho mipetraka",
    "rahampitso aho handeha",
    "tamin'ny volana lasa",
    "amin'ny taona ho avy",
    
    # Possession
    "ahy io boky io",
    "anao io vary io",
    "azy ny trano",
    "antsika ny fiainana",
    "anareo ny hevitra",
    "azy ireo ny tanàna",
    
    # Demandes et ordres
    "omeo rano aho",
    "omeo sakafo azy",
    "alao ity boky ity",
    "makà ity kapoaka ity",
    "manadìo ny trano",
    "manoratra taratasy",
    
    # Météo détaillée
    "be ny orana androany",
    "misy rivo-doza",
    "mangatsiaka ny maraina",
    "mafana ny mitataovovonana",
    "mangatsaka ny hariva",
    "maizina ny alina",
    
    # Sentiments avancés
    "be kivy aho noho ny vaovao ratsy",
    "faly loatra aho noho ny fahombiazana",
    "taitra aho tamin'ny zavatra hitako",
    "menatra aho amin'ny ataoko",
    "matahotra aho noho ny alina",
    
    # Santé
    "marary aho izao",
    "marary loha aho",
    "marary kibo aho",
    "tsara fahasalamana aho",
    "mandeha any amin'ny dokotera aho",
    
    # Loisirs
    "tiako ny mamaky boky",
    "tiako ny mihaino hira",
    "tiako ny mijery sarimihetsika",
    "tiako ny milalao baolina",
    "tiako ny mandeha an-tsangasanga",
    
    # Phrases complexes
    "raha tsara ny toetr'andro dia handeha any an-tsena aho",
    "rehefa vita ny asa dia hiverina any an-trano aho",
    "satria noana aho dia nihinana sakafo",
    "na dia reraka aza aho dia mitohy miasa ihany",
    "mba tonga haingana azafady",
    
    # Expressions courantes
    "tsara izany",
    "diso izany",
    "marina izany",
    "tsy mety izany",
    "azo atao izany",
    "tsy azo atao izany",
    "mety ho avy izy",
    "tsy maintsy handeha aho"
]


# ============================================================
# CORPUS SUPPLÉMENTAIRE (Bible, Proverbes)
# ============================================================

CORPUS_BIBLE = [
    "tia an'Andriamanitra sy ny namana",
    "manaja ny ray aman-dreny",
    "aoka ho tsara ny fo",
    "aoka ho tsara ny teny",
    "manomeza ny mahantra",
    "manampy ny sahirana",
    "mitady ny fahamarinana",
    "mandeha amin'ny lalana marina"
]

CORPUS_PROVERBES = [
    "ny marina tsy mba very",
    "ny mandainga tsy ho vanona",
    "ny mahay dia mandresy",
    "ny tsy mahay dia resy",
    "tsara ny fihavanana",
    "be ny olona be ny hevitra",
    "izay tia vola very soa"
]


# ============================================================
# FONCTION D'ENTRAÎNEMENT
# ============================================================

def train_ngram_model(corpus: list = None, n: int = 2, save_path: str = "data/ngram_model.json"):
    """
    Entraîne le modèle N-gram sur un corpus
    
    Args:
        corpus: Liste de phrases (si None, utilise le corpus par défaut)
        n: Taille des n-grams (2 = bigram, 3 = trigram)
        save_path: Chemin de sauvegarde du modèle
    """
    
    if corpus is None:
        corpus = CORPUS_MALAGASY + CORPUS_BIBLE + CORPUS_PROVERBES
    
    print("=" * 70)
    print(f"ENTRAÎNEMENT DU MODÈLE N-GRAM (n={n})")
    print("=" * 70)
    
    print(f"\n Corpus : {len(corpus)} phrases")
    
    # Créer et entraîner le modèle
    model = NGramModel(n=n)
    model.train(corpus)
    
    # Statistiques
    total_words = sum(len(text.split()) for text in corpus)
    unique_words = len(model.word_freq)
    total_ngrams = len(model.ngrams)
    
    print(f"\n Statistiques après entraînement :")
    print(f"   - Mots totaux : {total_words}")
    print(f"   - Mots uniques : {unique_words}")
    print(f"   - N-grams appris : {total_ngrams}")
    
    # Sauvegarder
    Path(save_path).parent.mkdir(exist_ok=True)
    model.save_model(save_path)
    print(f"\n Modèle sauvegardé : {save_path}")
    
    # Tests rapides
    print(f"\n Tests de prédiction :")
    
    test_contexts = [
        ["manao"],
        ["mihinana"],
        ["mandeha", "any"],
        ["tsara", "ny"]
    ]
    
    for context in test_contexts:
        predictions = model.predict_next_word(context, top_k=3)
        print(f"\n   Après '{' '.join(context)}' :")
        for word, prob in predictions:
            print(f"      - {word} ({prob:.1%})")
    
    print("\n" + "=" * 70)
    print(" ENTRAÎNEMENT TERMINÉ !")
    print("=" * 70)
    
    return model


# ============================================================
# AJOUT DE CORPUS PERSONNALISÉ
# ============================================================

def load_corpus_from_file(filepath: str) -> list:
    """
    Charge un corpus depuis un fichier texte
    Format : une phrase par ligne
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            corpus = [line.strip() for line in f if line.strip()]
        print(f" {len(corpus)} phrases chargées depuis {filepath}")
        return corpus
    except Exception as e:
        print(f" Erreur lors du chargement : {e}")
        return []


def enrich_corpus_from_wikipedia():
    """
    Enrichit le corpus avec les phrases des fichiers scrapés
    """
    corpus = []
    
    # Charger les fichiers de mots scrapés
    word_files = [
        "data/wikipedia_words.txt",
        "data/wikipedia_direct_words.txt",
        "data/bible_words.txt"
    ]
    
    for filepath in word_files:
        if Path(filepath).exists():
            words = load_corpus_from_file(filepath)
            # Créer des "phrases" simples de 3-5 mots
            for i in range(0, len(words) - 4, 3):
                phrase = " ".join(words[i:i+4])
                corpus.append(phrase)
    
    return corpus


# ============================================================
# SCRIPT PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("\n Options d'entraînement :")
    print("   1. Entraîner sur le corpus de base (200+ phrases)")
    print("   2. Entraîner sur corpus enrichi (base + Wikipedia)")
    print("   3. Charger un corpus depuis un fichier")
    
    choice = input("\n Votre choix (1-3) : ").strip()
    
    if choice == "1":
        train_ngram_model()
    
    elif choice == "2":
        print("\n Enrichissement du corpus...")
        base_corpus = CORPUS_MALAGASY + CORPUS_BIBLE + CORPUS_PROVERBES
        wiki_corpus = enrich_corpus_from_wikipedia()
        full_corpus = base_corpus + wiki_corpus
        print(f"   Corpus total : {len(full_corpus)} phrases")
        train_ngram_model(corpus=full_corpus)
    
    elif choice == "3":
        filepath = input(" Chemin du fichier : ").strip()
        custom_corpus = load_corpus_from_file(filepath)
        if custom_corpus:
            train_ngram_model(corpus=custom_corpus)
    
    else:
        print("X Choix invalide")
        print("ℹ  Entraînement avec corpus de base par défaut...")
        train_ngram_model()