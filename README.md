# cantonais.org

## Installation
1. Téléchargez pyenv et créez un environnement virtuel :
```
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

source ~/.zshrc

pyenv install 3.12.1
pyenv virtualenv cantonais_org
pyenv activate cantonais_org
```
2. Téléchargez les dépendances :
```
pip3 install -r requirements.txt
npm install
```
3. Téléchargez la base de données à partir de [jyutdictionary.com](https://jyutdictionary.com/#download-addon). Attention, le site est en anglais!
4. Définissez les variables d’environnement :
```
python3
>>> import uuid
>>> uuid.uuid4().hex
'<chaîne_de_caractères>'

export CANTONAIS_ORG_SECRET_KEY="<chaîne_de_caractères>"
export CANTONAIS_ORG_DB_PATH="<chemin_d'accès_de_la_base_de_données>"
```
5. Générez les actifs statiques :
```
purgecss --config purgecss.config.js
```
6. Lancez le serveur: `flask --app app run`

## Déploiement logiciel (sur Debian)
1. Installez nginx et supervisor: `sudo apt install nginx supervisor`
2. Créez le fichier `/etc/nginx/sites-enabled/cantonais_org` avec ces contenus :
```
server {
    listen 80;
    server_name <votre_adresse_ip_ou_nom_de_domaine_ici>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        include /etc/nginx/mime.types;
        root <chemin_d'accès_du_projet>;
        expires 30d;
        add_header Cache-Control "max-age=31536000";
    }
}
```
3. Dans le fichier `/etc/nginx/nginx.conf`, changez le paramètre « user » à votre nom d'utilisateur :
```
user <votre_nom_d'utilisateur_ici>;
worker_processes auto;
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;
```
4. Dans le fichier `/etc/nginx/nginx.conf`, changez les paramètres gzip afin de permettre la compression des données :
```
gzip on;

gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_buffers 16 8k;
gzip_http_version 1.1;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
gzip_min_length 256;
```
5. Relancez nginx avec la nouvelle configuration : `sudo nginx -s reload`
6. Créez le fichier `/etc/supervisor/conf.d/cantonais_org.conf` avec ces contenus :
```
[program:cantonais_org]
directory=<chemin_d'accès_de_ce_projet>
command=/bin/bash -c 'eval "$(pyenv init -)" && pyenv activate cantonais_org && gunicorn -w 5 wsgi:app'
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/cantonais_org/cantonais_org.err.log
stdout_logfile=/var/log/cantonais_org/cantonais_org.out.log
environment=PATH="/root/.pyenv/shims:/root/.pyenv/bin:%(ENV_PATH)s",PYENV_ROOT="/root/.pyenv",CANTONAIS_ORG_DB_PATH="<chemin_d'accès_de_la_base_de_données>",CANTONAIS_ORG_SECRET_KEY="chaîne_de_caractères"
user=root
```
7. Créez les fichiers de journalisation :
```
sudo mkdir /var/log/cantonais_org
sudo touch /var/log/cantonais_org/cantonais_org.out.log
sudo touch /var/log/cantonais_org/cantonais_org.err.log
```
8. Relancez supervisor : `sudo supervisorctl reload`
