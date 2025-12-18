# 🛠️ Outils Nécessaires pour le Projet

## Outils Obligatoires

### 1. Node.js et npm
**Pourquoi**: Exécuter React.js et gérer les dépendances
- **Version minimale**: Node.js 14.x ou supérieure
- **Téléchargement**: https://nodejs.org/
- **Installation**: Téléchargez la version LTS et suivez l'assistant
- **Vérification**:
```bash
node --version
npm --version
```

### 2. Éditeur de Code
**Pourquoi**: Modifier et développer le code

**Options recommandées**:

#### Visual Studio Code (Recommandé) ⭐
- **Téléchargement**: https://code.visualstudio.com/
- **Extensions recommandées**:
  - ES7+ React/Redux/React-Native snippets
  - Prettier - Code formatter
  - ESLint
  - Auto Rename Tag
  - Bracket Pair Colorizer

#### Alternatives:
- **WebStorm**: https://www.jetbrains.com/webstorm/ (payant, version étudiante gratuite)
- **Sublime Text**: https://www.sublimetext.com/
- **Atom**: https://atom.io/

### 3. Navigateur Web Moderne
**Pourquoi**: Tester l'application

**Options**:
- Google Chrome (Recommandé) - https://www.google.com/chrome/
- Mozilla Firefox - https://www.mozilla.org/firefox/
- Microsoft Edge
- Safari (macOS)

**Extensions navigateur utiles**:
- React Developer Tools
- Redux DevTools (si vous ajoutez Redux)

### 4. Terminal/Ligne de Commande
**Pourquoi**: Exécuter les commandes npm

**Selon votre OS**:
- **Windows**: 
  - PowerShell (intégré)
  - Git Bash (avec Git)
  - Windows Terminal (Microsoft Store)
- **macOS**: Terminal (intégré)
- **Linux**: Terminal (intégré)

## Outils Optionnels mais Recommandés

### 5. Git
**Pourquoi**: Gestion de versions et collaboration
- **Téléchargement**: https://git-scm.com/
- **Usage**:
```bash
git init
git add .
git commit -m "Initial commit"
```

### 6. Gestionnaire de Paquets Alternatifs

#### Yarn (Alternative à npm)
```bash
npm install -g yarn
```
**Avantages**: Plus rapide, meilleur cache

#### pnpm
```bash
npm install -g pnpm
```
**Avantages**: Économise de l'espace disque

### 7. Outils de Déploiement

#### Vercel CLI
```bash
npm install -g vercel
```
**Usage**: Déploiement rapide
```bash
vercel
```

#### Netlify CLI
```bash
npm install -g netlify-cli
```
**Usage**: Déploiement et tests locaux
```bash
netlify dev
```

### 8. Outils de Debug

#### React DevTools
- Extension Chrome/Firefox
- **Chrome**: https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi
- **Firefox**: https://addons.mozilla.org/firefox/addon/react-devtools/

#### Redux DevTools (si vous ajoutez Redux)
- Extension Chrome/Firefox
- **Chrome**: https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd

## Configuration de l'Environnement de Développement

### Windows

1. **Installer Node.js**
   - Téléchargez depuis nodejs.org
   - Exécutez l'installateur
   - Redémarrez votre ordinateur

2. **Installer Visual Studio Code**
   - Téléchargez depuis code.visualstudio.com
   - Installez les extensions recommandées

3. **Configurer Git (optionnel)**
   - Téléchargez depuis git-scm.com
   - Configurez:
   ```bash
   git config --global user.name "Votre Nom"
   git config --global user.email "votre@email.com"
   ```

### macOS

1. **Installer Homebrew** (gestionnaire de paquets)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Installer Node.js**
```bash
brew install node
```

3. **Installer Visual Studio Code**
```bash
brew install --cask visual-studio-code
```

### Linux (Ubuntu/Debian)

1. **Mettre à jour le système**
```bash
sudo apt update && sudo apt upgrade
```

2. **Installer Node.js et npm**
```bash
sudo apt install nodejs npm
```

3. **Installer Visual Studio Code**
```bash
sudo snap install code --classic
```

## Bibliothèques et Dépendances du Projet

Ces bibliothèques seront installées automatiquement avec `npm install`:

### Dépendances Principales
- **react**: ^18.2.0 - Framework principal
- **react-dom**: ^18.2.0 - Rendu DOM
- **react-scripts**: 5.0.1 - Scripts de build
- **react-quill**: ^2.0.0 - Éditeur de texte riche
- **quill**: ^1.3.7 - Moteur d'édition
- **axios**: ^1.6.0 - Requêtes HTTP (pour extensions futures)
- **lucide-react**: ^0.263.1 - Icônes
- **react-speech-recognition**: ^3.10.0 - Reconnaissance vocale (pour extensions)
- **regenerator-runtime**: ^0.14.0 - Support async/await

## Outils pour Extensions Futures

### Pour Scraping Web
```bash
npm install cheerio axios
```

### Pour Base de Données (MongoDB)
```bash
npm install mongodb mongoose
```

### Pour API Backend
```bash
npm install express cors body-parser
```

### Pour Tests
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

## Checklist de Préparation

Avant de commencer, vérifiez que vous avez:

- [ ] Node.js installé (version 14+)
- [ ] npm fonctionnel
- [ ] Éditeur de code installé (VS Code recommandé)
- [ ] Navigateur moderne installé
- [ ] Terminal/ligne de commande accessible
- [ ] Projet décompressé
- [ ] Dépendances installées (`npm install`)

## Ressources d'Apprentissage

### React.js
- Documentation officielle: https://react.dev
- Tutorial interactif: https://react.dev/learn
- FreeCodeCamp React: https://www.freecodecamp.org/learn/front-end-libraries/

### JavaScript ES6+
- MDN JavaScript: https://developer.mozilla.org/fr/docs/Web/JavaScript
- JavaScript.info: https://javascript.info/

### CSS et Design
- CSS-Tricks: https://css-tricks.com/
- Flexbox Froggy: https://flexboxfroggy.com/
- Grid Garden: https://cssgridgarden.com/

### Quill.js
- Documentation: https://quilljs.com/docs/
- Exemples: https://quilljs.com/playground/

## Support Technique

### Problèmes Courants

**Problème**: `npm` command not found
**Solution**: Réinstallez Node.js et redémarrez votre terminal

**Problème**: Port 3000 déjà utilisé
**Solution**: 
```bash
PORT=3001 npm start
```

**Problème**: Erreurs de dépendances
**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**Problème**: Erreur de mémoire lors du build
**Solution**:
```bash
NODE_OPTIONS=--max_old_space_size=4096 npm run build
```

## Commandes Utiles

```bash
# Installer les dépendances
npm install

# Lancer en développement
npm start

# Build de production
npm run build

# Lancer les tests
npm test

# Éjecter la configuration (ATTENTION: irréversible)
npm run eject

# Mettre à jour les dépendances
npm update

# Vérifier les vulnérabilités
npm audit

# Corriger les vulnérabilités
npm audit fix

# Nettoyer le cache npm
npm cache clean --force
```

## Conclusion

Avec ces outils installés, vous êtes prêt à développer l'éditeur de texte Malagasy ! 🚀

N'oubliez pas de consulter le README.md pour plus d'informations sur le projet et le GUIDE_INSTALLATION.md pour les instructions détaillées.

Bon développement ! 💻
