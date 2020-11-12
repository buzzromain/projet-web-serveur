## Commande
### Recupérer le dépôt
    git clone https://github.com/buzzromain/buzzromain-blog.git
    cd buzzromain-blog

### Initialiser l'environnement de développement
    make init-dev
    source venv/bin/activate

### Démarrer le serveur en mode développement
    make run-dev

### Commit une modification du code source en developpement
    make git m="description_modification"

### Deployer le serveur en production
    make deploy m="description_version"

### A faire
- [ ] Modeliser base de données SQL
- [ ] Creer le connecteur pour la base de données
- [ ] Creer les controleur
- [ ] Creer les vues