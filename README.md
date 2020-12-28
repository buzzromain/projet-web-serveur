# Projet web serveur
Projet realisé dans le cadre de nos études en Licence Informatique à l'Université Clermont Auvergne
Auteur : Romain G. / Nicolas D.

## Commande
Avant de saisir ces commandes, se placer dans le répertoire où l'on souhaite récuperer le dépôt.
### Recupérer le dépôt
    git clone https://github.com/buzzromain/projet-web-serveur.git
    cd projet-web-serveur

### Initialiser l'environnement de développement
    make init-dev
    source venv/bin/activate

### Démarrer le serveur en développement
    make run-dev

-------------------
Ne pas utiliser ces commandes dans l'immédiat.
### Recupérer les dernières modifications sur le depôt
    make git-pull
    
### Commit une modification du code source en developpement
    make git m="description_modification"

### Deployer le serveur en production
    make deploy m="description_version"

### A faire
- [X] Gérer les exceptions/code de status HTTP
- [X] Ajouter la modification de ressource "UPDATE"
- [ ] Faire l'interface en HTML/CSS/JS
- [ ] Relire le code source en entier