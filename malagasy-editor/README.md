# 🇲🇬 Éditeur de Texte Augmenté par l'IA pour le Malagasy

**Projet de TP Intelligence Artificielle - Institut Supérieur Polytechnique de Madagascar**

## 📋 Description

Application web d'édition de texte intelligente spécialement conçue pour la langue Malagasy, une langue à faibles ressources numériques. L'éditeur intègre plusieurs modules d'IA pour assister les rédacteurs malgaches avec des approches hybrides combinant méthodes symboliques, algorithmiques et data-driven.

## ✨ Fonctionnalités IA Implémentées

### 1. 📝 Correcteur Orthographique
- **Technologie**: Distance de Levenshtein + Dictionnaire
- **Fonctionnement**: Vérifie les mots en temps réel et suggère des corrections basées sur la similarité
- **Base de données**: Dictionnaire de ~100 mots malgaches courants (extensible)

### 2. ✅ Vérification Phonotactique
- **Technologie**: Règles linguistiques + REGEX
- **Fonctionnement**: Détecte les combinaisons de lettres impossibles en Malagasy (nb, mk, dt, bp, sz, nk)
- **Utilité**: Validation automatique de la structure des mots

### 3. 🔮 Autocomplétion (Next Word Prediction)
- **Technologie**: N-grams (Bigrammes)
- **Fonctionnement**: Prédit le prochain mot basé sur le contexte et les phrases communes
- **Corpus**: Bigrammes et trigrammes fréquents en Malagasy

### 4. 🌐 Traducteur Mot-à-Mot
- **Technologie**: Dictionnaire bilingue Malagasy ↔ Français
- **Fonctionnement**: Sélectionnez un mot pour voir sa traduction instantanée
- **Base**: ~80 mots avec traductions bidirectionnelles

### 5. 🔍 Lemmatisation (Recherche de Racine)
- **Technologie**: Analyse morphologique
- **Fonctionnement**: Retire les préfixes et suffixes pour trouver la racine du mot
- **Exemples**: 
  - manoratra → soratra
  - mihinana → hina
  - mampianatra → ianatra

### 6. 😊 Analyse de Sentiment
- **Technologie**: Bag of Words
- **Fonctionnement**: Classifie le texte comme Positif/Négatif/Neutre
- **Méthode**: Compte des mots positifs vs négatifs avec score en pourcentage

### 7. 🔊 Synthèse Vocale (TTS)
- **Technologie**: Web Speech API
- **Fonctionnement**: Lit le texte à voix haute avec accent malgache
- **Utilité**: Accessibilité et vérification de prononciation

## 🛠️ Technologies Utilisées

### Frontend
- **React.js 18.2** - Framework JavaScript
- **React Quill** - Éditeur de texte riche
- **Quill.js** - Moteur d'édition WYSIWYG
- **CSS3** - Animations et design moderne

### Algorithmes et IA
- **Distance de Levenshtein** - Correction orthographique
- **N-grams** - Prédiction de texte
- **Bag of Words** - Analyse de sentiment
- **Analyse morphologique** - Lemmatisation
- **REGEX** - Validation phonotactique

### APIs
- **Web Speech API** - Synthèse vocale

## 📦 Installation

### Prérequis
- Node.js (version 14 ou supérieure)
- npm ou yarn

### Étapes d'installation

1. **Décompresser le projet**
```bash
cd malagasy-editor
```

2. **Installer les dépendances**
```bash
npm install
```

3. **Lancer l'application en mode développement**
```bash
npm start
```

L'application sera accessible sur `http://localhost:3000`

4. **Build pour la production**
```bash
npm run build
```

## 📚 Structure du Projet

```
malagasy-editor/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Toolbar.js          # Barre d'outils
│   │   ├── Toolbar.css
│   │   ├── SidePanel.js        # Panneau latéral
│   │   └── SidePanel.css
│   ├── services/
│   │   ├── SpellChecker.js     # Correcteur orthographique
│   │   ├── AutoComplete.js     # Autocomplétion
│   │   ├── Translator.js       # Traduction
│   │   ├── SentimentAnalysis.js # Analyse sentiment
│   │   └── Lemmatizer.js       # Lemmatisation
│   ├── App.js                  # Composant principal
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🎯 Guide d'Utilisation

### Écrire du Texte
1. Tapez votre texte dans l'éditeur principal
2. Les suggestions de correction apparaissent automatiquement sous le texte
3. Les prédictions de mots s'affichent pendant la frappe

### Fonctionnalités IA

**Analyse de Sentiment** (😊)
- Cliquez sur le bouton "Sentiment"
- Le panneau latéral affiche le sentiment global et les mots détectés

**Traduction** (🌐)
- Sélectionnez un mot dans le texte
- Cliquez sur "Dika" pour voir la traduction

**Lemmatisation** (🔍)
- Sélectionnez un mot
- Cliquez sur "Faka" pour trouver sa racine

**Synthèse Vocale** (🔊)
- Cliquez sur "Vakio" pour entendre le texte lu à voix haute

### Formatage
- Utilisez la barre d'outils pour formater le texte (gras, italique, couleurs, etc.)
- Ajoutez des titres, listes, liens et images

## 🚀 Déploiement

### Déploiement sur Vercel
```bash
npm install -g vercel
vercel
```

### Déploiement sur Netlify
```bash
npm run build
# Glissez le dossier build/ dans Netlify
```

## 📖 Bibliographie et Sources

### Corpus de Données
- **Wikipedia Malagasy**: mg.wikipedia.org (~90k articles)
- **Teny Malagasy**: tenymalagasy.org (dictionnaire en ligne)
- **Baiboly Malagasy**: Corpus religieux

### Références Académiques
- Ranaivo-Malançon, B. (2006). "Computational analysis of Malagasy"
- Rasolofo, Y. & Savoy, J. (2002). "Term proximity scoring for keyword-based retrieval systems"

### Outils et Bibliothèques
- React Documentation: https://react.dev
- Quill.js: https://quilljs.com
- Levenshtein Distance Algorithm
- N-gram Language Models

### Ressources Linguistiques
- Structure morphologique du Malagasy
- Phonotactique et règles de formation des mots
- Préfixes: mi-, ma-, man-, mam-, maha-, mpan-, fi-, fan-, fam-
- Suffixes: -ana, -ina, -na

## 👥 Équipe de Développement

### Organisation Recommandée

**Squad Web/UI (2 personnes)**
- Design UX/UI
- Intégration React et Quill
- Responsive design
- Animations et interactions

**Squad Data/NLP (2 personnes)**
- Constitution des dictionnaires
- Algorithmes de correction
- Analyse morphologique
- Corpus et datasets

**Squad Algo/Backend (3 personnes)**
- Implémentation des services IA
- Distance de Levenshtein
- N-grams et prédiction
- Tests et optimisation

## 🎓 Critères d'Évaluation

| Critère | Poids | Détails |
|---------|-------|---------|
| **Fonctionnalités IA** | 40% | Pertinence du NLP malgré les contraintes |
| **UX** | 20% | Fluidité et intégration |
| **Qualité Technique** | 20% | Architecture et code |
| **Présentation** | 20% | Vidéo de démonstration |

## 🔧 Améliorations Possibles

### Court Terme
- [ ] Ajouter plus de mots au dictionnaire
- [ ] Scraper tenymalagasy.org pour enrichir la base
- [ ] Améliorer les bigrammes avec un corpus plus large
- [ ] Ajouter la reconnaissance d'entités (NER)

### Moyen Terme
- [ ] Intégrer une API de traduction externe
- [ ] Créer un Knowledge Graph pour l'exploration sémantique
- [ ] Ajouter un chatbot assistant
- [ ] Implémenter la reconnaissance vocale (STT)

### Long Terme
- [ ] Entraîner un modèle de langue personnalisé
- [ ] Base de données MongoDB pour les corpus
- [ ] API REST pour les services NLP
- [ ] Application mobile

## 📝 Licence

Projet académique - Institut Supérieur Polytechnique de Madagascar

## 📧 Contact

Pour toute question concernant ce projet, contactez l'équipe de développement.

---

**Créé avec ❤️ pour promouvoir la langue Malagasy dans le numérique**

*"Ny teny malagasy dia harena tokony hotahirizina"*
