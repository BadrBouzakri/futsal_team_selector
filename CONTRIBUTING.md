# Guide de Contribution

Merci de votre intérêt pour contribuer au Générateur d'Équipes Futsal ! 🏆

## Comment contribuer

### Signaler un bug 🐛

1. Vérifiez que le bug n'a pas déjà été signalé dans les [issues](https://github.com/BadrBouzakri/futsal_team_selector/issues)
2. Créez une nouvelle issue avec :
   - Une description claire du problème
   - Les étapes pour reproduire le bug
   - Votre environnement (OS, navigateur, version Docker)
   - Des captures d'écran si pertinentes

### Proposer une amélioration ✨

1. Ouvrez une issue pour discuter de votre idée
2. Attendez les commentaires avant de commencer le développement
3. Suivez le processus de pull request ci-dessous

### Processus de Pull Request

1. **Fork** le repository
2. **Clonez** votre fork :
   ```bash
   git clone https://github.com/VOTRE_USERNAME/futsal_team_selector.git
   cd futsal_team_selector
   ```

3. **Créez une branche** pour votre fonctionnalité :
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   ```

4. **Développez** votre fonctionnalité :
   - Respectez le style de code existant
   - Ajoutez des commentaires si nécessaire
   - Testez vos modifications localement

5. **Committez** vos changements :
   ```bash
   git add .
   git commit -m "✨ Ajout de ma nouvelle fonctionnalité"
   ```

6. **Poussez** vers votre fork :
   ```bash
   git push origin feature/ma-nouvelle-fonctionnalite
   ```

7. **Créez une Pull Request** sur GitHub

## Standards de code

### Python
- Suivez les conventions PEP 8
- Utilisez des noms de variables explicites
- Ajoutez des docstrings pour les fonctions complexes
- Limitez les lignes à 80 caractères quand possible

### HTML/CSS
- Utilisez l'indentation à 4 espaces
- Organisez le CSS de manière logique
- Commentez les sections complexes
- Assurez-vous de la compatibilité mobile

### JavaScript
- Utilisez des noms de fonctions explicites
- Commentez la logique complexe
- Évitez les variables globales
- Testez sur différents navigateurs

## Tests

Avant de soumettre votre PR :

1. **Testez localement** :
   ```bash
   python app.py
   # Vérifiez que tout fonctionne sur http://localhost:5050
   ```

2. **Testez avec Docker** :
   ```bash
   ./start.sh docker
   # Vérifiez que l'application démarre correctement
   ```

3. **Testez sur mobile** :
   - Utilisez les outils de développement du navigateur
   - Vérifiez la responsivité

## Types de contributions

### 🎆 Nouvelles fonctionnalités
- Nouvelles méthodes d'équilibrage
- Améliorations de l'interface
- Nouvelles statistiques
- Intégrations externes

### 🎨 Améliorations UI/UX
- Nouveaux thèmes ou couleurs
- Animations améliorées
- Accessibilité
- Performance

### 📄 Documentation
- Amélioration du README
- Ajout d'exemples
- Traductions
- Guides d'utilisation

### 🐛 Corrections de bugs
- Correction d'erreurs
- Amélioration de la stabilité
- Optimisations

## Structure du projet

```
futsal_team_selector/
├── app.py                 # Application principale
├── config.py              # Configuration
├── templates/             # Templates HTML
│   ├── index.html         # Page d'accueil
│   ├── teams.html         # Affichage équipes
│   ├── history.html       # Historique
│   └── admin*.html        # Administration
├── static/               # Fichiers statiques (si ajoutés)
├── requirements.txt      # Dépendances Python
├── Dockerfile            # Configuration Docker
└── start.sh             # Script de démarrage
```

## Conventions de commit

Utilisez des emojis pour clarifier le type de commit :

- ✨ `:sparkles:` Nouvelle fonctionnalité
- 🐛 `:bug:` Correction de bug
- 📝 `:memo:` Documentation
- 🎨 `:art:` Amélioration UI/style
- ⚡ `:zap:` Amélioration performance
- 🔧 `:wrench:` Configuration
- 🚀 `:rocket:` Déploiement
- ❇️ `:heavy_plus_sign:` Ajout de dépendance
- ➖ `:heavy_minus_sign:` Suppression
- 🔒 `:lock:` Sécurité

Exemple :
```bash
git commit -m "✨ Ajout de la fonction d'export PDF des équipes"
```

## Questions et support

- 💬 Discussions : Utilisez les [Discussions GitHub](https://github.com/BadrBouzakri/futsal_team_selector/discussions)
- 🐛 Bugs : Créez une [issue](https://github.com/BadrBouzakri/futsal_team_selector/issues)
- ❓ Questions : Demandez dans les discussions ou par email

## Code de conduite

- Soyez respectueux envers tous les contributeurs
- Utilisez un langage inclusif et professionnel
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est le mieux pour la communauté

## Reconnaissance

Tous les contributeurs seront ajoutés à la section "Contributeurs" du README. Merci de faire partie de ce projet ! 🚀

---

**Merci de contribuer au Générateur d'Équipes Futsal !** 🏆⚽