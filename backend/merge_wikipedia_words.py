from pathlib import Path
import re

MALAGASY_WORDS = Path("data/malagasy_words.txt")
WIKI_WORDS = Path("data/wikipedia_direct_words.txt")

def normalize_word(word: str) -> str:
    """Nettoie un mot (minuscule + lettres uniquement)"""
    word = word.lower().strip()
    word = re.sub(r"[^a-zàâôôéèêîïûùç']", "", word)
    return word

def load_words(filepath: Path) -> set:
    """Charge les mots valides d'un fichier .txt"""
    words = set()

    if not filepath.exists():
        print(f"❌ Fichier introuvable : {filepath}")
        return words

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            word = normalize_word(line)
            if word:
                words.add(word)

    return words

def merge_wikipedia_into_dictionary():
    print("📥 Chargement des mots existants...")
    existing_words = load_words(MALAGASY_WORDS)

    print("📥 Chargement des mots Wikipedia...")
    wiki_words = load_words(WIKI_WORDS)

    new_words = wiki_words - existing_words

    if not new_words:
        print("ℹ Aucun nouveau mot à ajouter")
        return

    print(f"➕ {len(new_words)} nouveaux mots trouvés")

    with open(MALAGASY_WORDS, "a", encoding="utf-8") as f:
        f.write("\n\n# ===== MOTS AJOUTÉS DEPUIS WIKIPEDIA =====\n")
        for word in sorted(new_words):
            f.write(word + "\n")

    print("✅ Fusion terminée avec succès")

if __name__ == "__main__":
    merge_wikipedia_into_dictionary()
