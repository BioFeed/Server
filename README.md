# Serveur Flask #

## Introduction ##  
Flask est un framework python facile à prendre en main et à utiliser. Il est assez puissant pour gérer de gros projets. 
En plus tout est en python donc c'est lisible. La documentation est disponible 
[ici](https://flask.palletsprojects.com/en/2.3.x/).

## Utilisation ##
Après avoir cloné le projet, il reste quelques étapes avant de pouvoir lancer le serveur. Pour cela il suffit de faire :
```sh 
make init
```

Pour lancer le serveur flask, exécuter la commande : 
```sh 
flask --app app.py run
```

## Tests ##
Des tests ont été implémentés dans le `Makefile`, pour l'utiliser, il faut d'abord le configurer. Directement sur le 
serveur, lancez le script `generate_tokens.py` qui se trouve dans le dossier `modules/`. Récupérez la chaîne de
caractères aléatoire et stockez là. C'est grâce à ce token que l'on peut envoyer des requêtes au serveur. Il faudra pour 
les tests la rentrer dans la variable `TOKEN` du `Makefile`. N'oubliez pas de la supprimer une fois les tests finis !
Remplissez le reste des informations et lancez `make test` ou `make test_local` pour effectuer les tests.  

Informations à modifier : 
```makefile
TOKEN=X9oIrX4UlQsjY5P0XXtO
DISTANT_URL=biofeed.vitavault.fr
DISTANT_PORT=443
LOCAL_URL=localhost
LOCAL_PORT=5000
```

La version locale correspond aux tests effectués directement sur le serveur. Par exemple en testant directement le
script sur son ordinateur. 

## Tokens ##  
L'objectif est de se rapprocher du fonctionnement des JWT (Json Web Token). Plusieurs idées pourront être implémentées :
- mettre un timeout sur les tokens (utilisation de date) pour revoke l'accès après un temps limite
- mettre un nombre de requêtes max pour éviter le DDOS
- chiffrer les transferts de données

```
$ python modules/generate_tokens.py 
Random String: umZl6ZA881Jx7tDSyryO  <-- token privé à garder 
Hash: 9c219dc12d3ea6022aa66f944e131394aacaee8122bc9e72dd59ff812b9ccdec  <-- hash stocké sur le serveur
```

### Utilisation 
Pour l'instant, la vérification se fait simplement en regardant si le JSON envoyé contient un champ "token" et que le 
token contenu est dans `token.json`. 

```sh
curl -X POST -H "Content-Type: application/json" -d \ 
'{"command": "clear", "token": "umZl6ZA881Jx7tDSyryO"}' \
http://localhost:5000/command
```

