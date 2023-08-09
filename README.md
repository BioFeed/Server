# Serveur Flask #

## Introduction ##  
Flask est un framework python facile à prendre en main et à utiliser. Il est assez puissant pour gérer de gros projets. 
En plus tout est en python donc c'est lisible. La documentation est disponible 
[ici](https://flask.palletsprojects.com/en/2.3.x/).

## Utilisation ##
Après avoir cloné le projet, préparer le serveur avec `chmod +x init.sh && ./init.sh`.

Pour lancer le serveur flask, exécuter la commande : 
```sh 
flask --app app.py run
```


## Tests ##
Pour lancer les tests il suffit de lancer `python tests.py` avec les bonnes informations en début de script. 

Les tests sont configurables : 
```python 
tests = [
            (
                {"name": "carotte", "date": 1234, "photo": "base64ici", "token": TOKEN}, # <-- informations
                '/store_data' # <-- page à acceder 
            ), 
            ...
        ]
```
Le script envoie les requêtes et vérifie si le serveur renvoie 200, ce qui est sensé être le cas pour toutes les 
requêtes.

Informations à modifier : 
```python
TOKEN = 'X9oIrX4UlQsjY5P0XXtO'
DISTANT_URL = 'biofeed.vitavault.fr'
DISTANT_PORT = 443
LOCAL_URL = 'localhost'
LOCAL_PORT = 5000
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

