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

## Gogs installation

1. Create MySQL and setup gogs user
```
SET @s = IF(version() < 8 OR (version() LIKE '%MariaDB%' AND version() < 10.3),
            'SET GLOBAL innodb_file_per_table = ON,
                        innodb_file_format = Barracuda,
                        innodb_large_prefix = ON;',
            'SET GLOBAL innodb_file_per_table = ON;');
PREPARE stmt1 FROM @s;
EXECUTE stmt1;

DROP DATABASE IF EXISTS gogs;
CREATE DATABASE IF NOT EXISTS gogs CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER gogs IDENTIFIED BY 'WRITE A PASSWORD FOR DATABASE USER GOGS HERE';
RANT ALL PRIVILEGES ON gogs.* TO gogs with grant option;
FLUSH PRIVILEGES;
EXIT;
```
2. Install other prerequisities -> https://gogs.io/docs/installation
3. Get the latest archive from https://github.com/gogs/gogs/releases
4. Install gogs
```
sudo adduser --disabled-login --gecos 'Gogs' git
sudo su - git
# extract the archive in git home folder
./gogs web
```
Go to server ip:3000 and setup database + admin account (write down login details somewhere) :
```
    Database type = MySQL
    Host = 127.0.0.1:3306
    User = gogs
    Password = WRITE A PASSWORD FOR DATABASE USER GOGS HERE
    Database Name = gogs
```
All the other settings can be random (we will change them manually in app.ini)
5. Configure gogs : in git home folder, edit `gogs/conf/custom/app.ini` : 
Replace vitavault.fr by whatever domain you are using.
```
BRAND_NAME = Gogs
RUN_USER   = git
RUN_MODE   = prod

[database]
TYPE     = mysql
HOST     = 127.0.0.1:3306
NAME     = gogs
SCHEMA   = public
USER     = gogs
PASSWORD = WRITE A PASSWORD FOR DATABASE USER GOGS HERE # Should already be there
SSL_MODE = disable
PATH     = /home/git/gogs/data/gogs.db

[repository]
ROOT           = /home/git/gogs-repositories
DEFAULT_BRANCH = master

[server]
PROTOCOL         = http
DOMAIN           = gogs.vitavault.fr
ROOT_URL         = https://gogs.vitavault.fr/
EXTERNAL_URL     = https://gogs.vitavault.fr/
HTTP_ADDR        = 127.0.0.1
HTTP_PORT        = 3000
DISABLE_SSH      = true
SSH_PORT         = 22
START_SSH_SERVER = false
OFFLINE_MODE     = false

[mailer]
ENABLED = false

[auth]
REQUIRE_EMAIL_CONFIRMATION  = false
DISABLE_REGISTRATION        = true # This is important for security
ENABLE_REGISTRATION_CAPTCHA = true
REQUIRE_SIGNIN_VIEW         = false

[user]
ENABLE_EMAIL_NOTIFICATION = false

[picture]
DISABLE_GRAVATAR        = false
ENABLE_FEDERATED_AVATAR = false

[session]
PROVIDER = file

[log]
MODE      = file
LEVEL     = Info
ROOT_PATH = /home/git/gogs/log

[security]
INSTALL_LOCK = true
SECRET_KEY   = .... # no need to change yours
```
6. Setup apache config 
Lookup how to create a website conf file using Apache and use certbot to generate SSL certificates.
My final config looks like this :
```
<VirtualHost *:443>
    ServerName gogs.vitavault.fr    
    ServerAlias gogs.vitavault.fr
    ProxyPreserveHost On
    ProxyRequests off
    ProxyPass / http://127.0.0.1:3000/ # / at the end is very important
    ProxyPassReverse / http://127.0.0.1:3000/ # same here

    <Proxy *>
        Order allow,deny
        Allow from all
    </Proxy>

    # The following lines were generated using sudo certbot --apache...
    SSLCertificateFile /etc/letsencrypt/live/gogs.vitavault.fr-0001/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/gogs.vitavault.fr-0001/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
```
My main website config is :
```
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	ServerName vitavault.fr
	DocumentRoot /var/www/html
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
	ServerAdmin webmaster@localhost
        ServerName vitavault.fr
	DocumentRoot /var/www/html
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

SSLCertificateFile /etc/letsencrypt/live/vitavault.fr/fullchain.pem
SSLCertificateKeyFile /etc/letsencrypt/live/vitavault.fr/privkey.pem
Include /etc/letsencrypt/options-ssl-apache.conf
</VirtualHost>
</IfModule>
```
Make sure there is no .htaccess in /var/www/html that is messing up redirections.

Finally lookup how to create a gogs systemd service !
