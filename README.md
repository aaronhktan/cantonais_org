# cantonais.org

## Installation
1. Téléchargez pyenv et créez un environnement virtuel:
```
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

pyenv install 3.12.1
pyenv virtualenv cantonais_org
pyenv activate cantonais_org
```
2. Téléchargez les dépendances:
```
pip3 install -r requirements.txt
```
3. Téléchargez la base de données à partir de [jyutdictionary.com](https://jyutdictionary.com/#download-addon). Attention, le site est en anglais!
4. Définissez les variables d’environnement:
```
python3
>>> import uuid
>>> uuid.uuid4().hex
'<chaîne_de_caractères>'

export export CANTONAIS_ORG_SECRET_KEY="<chaîne_de_caractères>"
export CANTONAIS_ORG_DB_PATH="<chemin_d'accès_de_la_base_de_données>"
```
5. Lancez le serveur: `flask --app app run`

## Déploiement logiciel (sur Debian)
1. Installez nginx, supervisor et gunicorn: `sudo apt install nginx supervisor gunicorn`
2. Créez le fichier `/etc/nginx/sites-enabled/cantonais_org` avec ces contenus:
```
server {
    listen 80;
    server_name <votre_adresse_ip_ici>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
3. Relancez nginx avec la nouvelle configuration: `sudo nginx -s reload`
4. Créez le fichier `/etc/supervisor/conf.d/cantonais_org.conf` avec ces contenus:
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
5. Créez les fichiers de journalisation:
```
sudo mkdir /var/log/cantonais_org
sudo touch /var/log/cantonais_org/cantonais_org.out.log
sudo touch /var/log/cantonais_org/cantonais_org.err.log
```
6. Relancez supervisor: `sudo supervisorctl reload`
