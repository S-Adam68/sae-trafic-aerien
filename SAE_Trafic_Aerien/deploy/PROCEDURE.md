# Fiche de procédure - Trafic Aerien

Projet SAÉ RT - architecture 2 VM:

- VM 1: serveur web Debian, Django, Gunicorn, Nginx
- VM 2: serveur MariaDB
- accès extérieur uniquement via la VM 1 sur le port 80
- communication entre les deux VM sur un réseau interne

## 1. VM 2 - serveur de base de données

```bash
apt update
apt install mariadb-server
```

Modifier la configuration de MariaDB:

```bash
nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Remplacer:

```ini
bind-address = 127.0.0.1
```

par:

```ini
bind-address = 0.0.0.0
```

Puis redémarrer:

```bash
systemctl restart mariadb
```

Créer la base et l'utilisateur:

```bash
mysql -u root
CREATE DATABASE trafic_aerien_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'trafic_user'@'[IP_VM_DJANGO]' IDENTIFIED BY 'motdepasseSAE';
GRANT ALL PRIVILEGES ON trafic_aerien_db.* TO 'trafic_user'@'[IP_VM_DJANGO]';
FLUSH PRIVILEGES;
EXIT;
```

Restaurer une sauvegarde éventuelle:

```bash
mysql -u root trafic_aerien_db < sauvegarde_trafic_aerien.sql
```

## 2. VM 1 - serveur web

Installer les dépendances système:

```bash
apt update
apt install python3-venv python3-pip nginx default-libmysqlclient-dev pkg-config build-essential git
```

Récupérer le code source puis se placer dans le projet:

```bash
cd /home/toto/
git clone <URL_DU_DEPOT>
cd SAE_Trafic_Aerien
```

Configurer `trafic_aerien/settings.py`:

- `ALLOWED_HOSTS = ['[IP_VM_DJANGO]', 'localhost']`
- `DATABASES['default']['HOST'] = '[IP_VM_SQL]'`

Créer l'environnement Python et lancer Gunicorn:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
gunicorn trafic_aerien.wsgi:application --bind 127.0.0.1:8000 --daemon
```

Configurer Nginx:

```bash
nano /etc/nginx/sites-available/trafic_aerien
```

Exemple:

```nginx
server {
    listen 80;
    server_name [IP_VM_DJANGO];
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static/ {
        alias /home/toto/SAE_Trafic_Aerien/static/;
    }
    location /media/ {
        alias /home/toto/SAE_Trafic_Aerien/media/;
    }
}
```

Activer le site:

```bash
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/trafic_aerien /etc/nginx/sites-enabled/
systemctl restart nginx
```

## 3. Vérifications

```bash
systemctl status nginx
systemctl status mariadb
mysql -u trafic_user -p -h [IP_VM_SQL] trafic_aerien_db
```

Accès attendu:

```text
http://[IP_VM_DJANGO]/
http://[IP_VM_DJANGO]/admin/
```