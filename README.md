# Serveur Flask #

## Introduction ##  
Flask est un framework python facile à prendre en main et à utiliser. Il est assez puissant pour gérer de gros projets. 
En plus tout est en python donc c'est lisible. La documentation est disponible 
[ici](https://flask.palletsprojects.com/en/2.3.x/).

## Tokens ##  
L'objectif est de se rapprocher du fonctionnement des JWT (Json Web Token). Plusieurs idées pourront être implémentées :
- mettre un timeout sur les tokens (utilisation de date) pour revoke l'accès après un temps limite
- mettre un nombre de requêtes max pour éviter le DDOS
- chiffrer les transferts de données 

### Utilisation 
Pour l'instant, la vérification se fait simplement en regardant si le JSON envoyé contient un champ "token" et que le 
token contenu est dans `token.json`. Pour créer un token, il faut lancer `generate_token.py` sur le serveur et copier
le token en clair. C'est celui-là qu'il faudra rajouter à la requête JSON. 

Pour lancer le serveur flask, exécuter la commande : `flask --app app.py run`
