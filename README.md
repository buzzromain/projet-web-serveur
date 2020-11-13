## Commande
Avant de saisir ces commandes, se placer dans le répertoire où l'on souhaite récuperer le dépôt.
### Recupérer le dépôt
    git clone https://github.com/buzzromain/buzzromain-blog.git
    cd buzzromain-blog

### Initialiser l'environnement de développement
    make init-dev
    source venv/bin/activate

### Démarrer le serveur en développement
    make run-dev

-------------------
Ne pas utiliser ces commandes dans l'immédiat.
### Commit une modification du code source en developpement
    make git m="description_modification"

### Deployer le serveur en production
    make deploy m="description_version"

### A faire
- [ ] Modeliser base de données SQL
- [ ] Creer le connecteur pour la base de données
- [ ] Creer les controleur
- [ ] Creer les vues