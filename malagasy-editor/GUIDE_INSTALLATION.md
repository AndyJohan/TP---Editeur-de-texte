# 📘 Guide d'Installation Complet

## Installation de Node.js et npm

### Windows
1. Téléchargez Node.js depuis https://nodejs.org/
2. Installez la version LTS (recommandée)
3. Vérifiez l'installation:
```cmd
node --version
npm --version
```

### macOS
```bash
# Avec Homebrew
brew install node

# Vérification
node --version
npm --version
```

### Linux (Ubuntu/Debian)
```bash
# Installation
sudo apt update
sudo apt install nodejs npm

# Vérification
node --version
npm --version
```

## Installation du Projet

### Méthode 1: Décompression du ZIP
1. Décompressez le fichier `malagasy-editor.zip`
2. Ouvrez un terminal dans le dossier décompressé
3. Installez les dépendances:
```bash
npm install
```

### Méthode 2: Clone depuis Git
```bash
git clone [votre-repo]
cd malagasy-editor
npm install
```

## Lancement de l'Application

### Mode Développement
```bash
npm start
```
- L'application s'ouvre automatiquement sur `http://localhost:3000`
- Les modifications du code sont rechargées automatiquement

### Build de Production
```bash
npm run build
```
- Crée un dossier `build/` optimisé
- Prêt pour le déploiement

## Dépannage

### Erreur "npm not found"
- Réinstallez Node.js
- Vérifiez que npm est dans votre PATH

### Erreur de port déjà utilisé
```bash
# Changez le port dans package.json ou utilisez:
PORT=3001 npm start
```

### Problèmes de dépendances
```bash
# Nettoyez et réinstallez
rm -rf node_modules package-lock.json
npm install
```

## Déploiement

### Sur Vercel (Recommandé)
1. Créez un compte sur https://vercel.com
2. Installez Vercel CLI:
```bash
npm install -g vercel
```
3. Déployez:
```bash
vercel
```

### Sur Netlify
1. Buildez l'application:
```bash
npm run build
```
2. Glissez le dossier `build/` sur https://app.netlify.com/drop

### Sur GitHub Pages
1. Installez gh-pages:
```bash
npm install --save-dev gh-pages
```
2. Ajoutez dans package.json:
```json
"homepage": "https://votre-username.github.io/malagasy-editor",
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}
```
3. Déployez:
```bash
npm run deploy
```

## Tests

### Lancer les tests
```bash
npm test
```

### Vérifier la couverture
```bash
npm test -- --coverage
```

## Support

En cas de problème:
1. Vérifiez les versions de Node.js et npm
2. Consultez les logs d'erreur
3. Vérifiez les issues GitHub
4. Contactez l'équipe

Bonne chance avec votre projet ! 🚀
