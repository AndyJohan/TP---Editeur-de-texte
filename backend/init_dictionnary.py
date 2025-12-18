"""
Script d'initialisation du dictionnaire Malagasy.
À exécuter UNE SEULE FOIS au début du projet.
"""

import os
from pathlib import Path

def create_malagasy_words_file():
    """Crée le fichier data/malagasy_words.txt avec les mots de base"""
    
    # Créer le dossier data s'il n'existe pas
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    words_file = data_dir / "malagasy_words.txt"
    
    # Liste des mots de base (500+ mots)
    base_words = """# Fichier: data/malagasy_words.txt
# Liste de mots malagasy courants (un mot par ligne)

# PRONOMS
aho
ianao
izy
isika
izahay
ianareo
izireo

# VERBES COURANTS
manao
mandeha
mipetraka
mihinana
misotro
matory
mifoha
miasa
mianatra
mampianatra
manasa
mandidy
miteny
milaza
manontany
mamaky
manoratra
mijery
mihaino
mahita
mahare
mahalala
mahafantatra
manome
mandray
mivarotra
mividy
mikapoka
miditra
mivoaka
mitsangana
mihazakazaka
mandehandeha
mitsidika
mangataka
manadio
manampy
manokatra
mihidy
mamaha
mamela
mandany
mitahiry
mameno
mamafy
mamboly
manangona
mandoro
miverina
mijanona
mamindra
manova
mandinika
mamorona
manamboatra
mandoa

# NOMS - FAMILLE
ray
reny
zanaka
rahalahy
rahavavy
zoky
zandry
dadabe
nenibe
zafikely
havana
fianakaviana
vady

# NOMS - CORPS
loha
maso
sofina
orona
vava
nify
lela
vozona
soroka
tanana
tongotra
vatana
fo
aty
ra

# NOMS - MAISON
trano
efitra
varavarankely
varavaran
rihana
latabatra
seza
fandriana
lamosina
tafo
rindrina
tokotany
tohatra
vavahady

# NOMS - NOURRITURE
sakafo
vary
hena
trondro
akoho
mofo
ronono
toaka
divay
dite
rano
ranomamy
sakay
sira
siramamy
voankazo
legioma
voatabia
akondro
anana
breda

# NOMS - NATURE
tany
lanitra
masoandro
volana
kintana
rahona
orana
rivotra
ranomasina
renirano
tendrombohitra
hazo
ahitra
voninkazo
vato
fasika
afo

# ADJECTIFS
tsara
ratsy
lehibe
kely
lava
fohy
mainty
fotsy
mena
manga
mavo
maintso
malemy
mafy
mafana
mangatsiaka
maina
lena
mando
masaka
matsatso
madio
maloto
vaovao
antitra
tanora
be
vitsy
feno
foana
lalina
marivo
avo
ambany
haingana
miadana
mora
sarotra
mendrika

# ADVERBES
tsara
ratsy
haingana
miadana
foana
indrindra
loatra
mihitsy
tokoa
koa
ihany
aza
tsy
mbola
efa
dia

# PRÉPOSITIONS
amin'ny
amin
eo
any
aty
avy
ho
ao
ambony
ambany
anaty
anilan
talohan
aorian
manodidina

# CONJONCTIONS
sy
ary
na
fa
kanefa
nefa
satria
raha
rehefa
nony
mandra
ambara

# INTERROGATIFS
ahoana
iza
inona
aiza
oviana
rahoviana
nahoana
firy

# TEMPS
omaly
androany
rahampitso
maraina
mitataovovonana
tolakandro
hariva
alina
mamatonalina
andro
herinandro
volana
taona
fotoana

# NOMBRES
iray
roa
telo
efatra
dimy
enina
fito
valo
sivy
folo
roapolo
telopolo
zato
arivo
alina
tapitrisa

# COULEURS
mainty
fotsy
mena
manga
maitso
mavo

# ANIMAUX
alika
saka
akoho
omby
kisoa
ondry
osy
soavaly
ampondra
vorona
trondro
biby

# PROFESSIONS
mpampianatra
mpianatra
dokotera
mpitsabo
mpanamboatra
mpitarika
mpiasa
mpividy
mpivarotra
mpamboly
mpitaiza
mpanoratra

# MOTS FRÉQUENTS
tsy
tsia
eny
mety
tonga
lasa
vita
mbola
efa
dia
koa
ihany
izao
izany
io
ity
fa
raha
marina
diso
tsara
zavatra
olona
toerana
fotoana

# SALUTATIONS
manao
ahoana
salama
veloma
misaotra
azafady

# DIRECTIONS
avaratra
atsimo
atsinanana
andrefana
ankavanana
ankavia

# VILLES
antananarivo
toamasina
antsirabe
mahajanga
toliara
fianarantsoa
antsiranana
morondava

# VERBES ACTION
mamono
mamelona
mandady
manangana
mandrava
manavao
manamarina
mandainga
manambara
manafina
mitady
mahita
manome
maka
misintona
manosika
manaikitra
manapaka
mameno
manafoana

# ÉMOTIONS
faly
malahelo
sosotra
taitra
menatra
sahy
matahotra
mangetaheta
"""
    
    # Écrire le fichier
    with open(words_file, 'w', encoding='utf-8') as f:
        f.write(base_words)
    
    # Compter les mots
    word_count = len([line for line in base_words.split('\n') 
                      if line.strip() and not line.strip().startswith('#')])
    
    print(f"Fichier créé : {words_file}")
    print(f"Nombre de mots : {word_count}")
    
    return words_file


def test_dictionary():
    """Test le dictionnaire avec quelques exemples"""
    from nlp.dictionary_loader import MalagasyDictionary
    
    print("\n" + "=" * 60)
    print("TEST DU DICTIONNAIRE")
    print("=" * 60)
    
    dictionary = MalagasyDictionary()
    stats = dictionary.get_statistics()
    
    print(f"\nStatistiques :")
    print(f"   - Total de mots : {stats['total_words']}")
    print(f"   - Avec définitions : {stats['words_with_definitions']}")
    
    print(f"\n Tests de validation :")
    
    test_words = [
        ("manao", True),
        ("aho", True),
        ("tsara", True),
        ("blabla", False),
        ("xyzqw", False),
        ("mihinana", True),
        ("tsy", True)
    ]
    
    for word, should_exist in test_words:
        exists = dictionary.word_exists(word)
        status = "V" if exists == should_exist else "X"
        print(f"   {status} '{word}' : {exists} (attendu: {should_exist})")


def main():
    """Fonction principale d'initialisation"""
    print("=" * 60)
    print("INITIALISATION DU PROJET MALAGASY NLP")
    print("=" * 60)
    
    print("\n Étape 1 : Création du fichier de mots...")
    words_file = create_malagasy_words_file()
    
    print("\n Étape 2 : Test du dictionnaire...")
    test_dictionary()
    
    print("\n" + "=" * 60)
    print(" INITIALISATION TERMINÉE !")
    print("=" * 60)
    
    print("\n Prochaines étapes :")
    print("   1. Testez symbolic.py : python nlp/symbolic.py")
    print("   2. Ajoutez plus de mots dans data/malagasy_words.txt si nécessaire")
    print("   3. Intégrez dans votre API/Frontend")
    
    print("\n Conseil : Pour enrichir le dictionnaire, vous pouvez :")
    print("   - Ajouter manuellement des mots fréquents")
    print("   - Scraper Wikipedia MG (voir dictionary_loader.py)")
    print("   - Extraire des mots de corpus existants (Bible, journaux)")


if __name__ == "__main__":
    main()