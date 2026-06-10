# SAE Trafic Aérien — IUT Réseaux & Télécommunications 2025-2026

Application web de gestion du trafic aérien développée en Python/Django dans le cadre de la SAÉ 2.03.

**Équipe :** Adam Sebar · Jordan · Yacine  
**Dépôt public accessible en lecture jusqu'à fin juin 2026**

---

## Contenu du dépôt

| Dossier / Fichier | Description |
|---|---|
| `SAE_Trafic_Aerien/` | Code source complet de l'application Django |
| `docs/gantt.html` | Diagramme de Gantt (ouvrir dans un navigateur) |
| `docs/schema_relationnel.md` | Schéma relationnel de la base de données |
| `docs/creation_tables.sql` | Script SQL : création des tables + insertion de données |
| `deploy/nginx.conf` | Configuration Nginx (reverse proxy VM1) |
| `deploy/gunicorn.service` | Service systemd Gunicorn (VM1) |
| `deploy/mariadb.sql` | Script de configuration MariaDB (VM2) |
| `SAE_Trafic_Aerien/populate.py` | Script de peuplement de la base de données |

---

## Architecture

```
Navigateur client
      |  HTTP port 80
      v
VM 1 — Serveur Web (Debian)
  Nginx (reverse proxy) -> Gunicorn -> Django 6.0.5
      |  SQL port 3306 (réseau interne)
      v
VM 2 — Base de données (Debian)
  MariaDB — base : trafic_aerien_db
```

---

## Fonctionnalités principales

- Gestion des **aéroports** et de leurs **pistes** (longueur, numéro)
- Gestion des **compagnies aériennes**, **types d'avions** et **avions**
- Gestion des **vols** avec affectation automatique de piste :
  - Vérifie la compatibilité longueur piste / type d'avion
  - Bloque la piste ±10 min autour de chaque atterrissage
  - Suggère un décalage de +15 min si aucune piste disponible
- **Fiche des vols** : recherche par aéroport, plage de dates, direction
- **Import CSV** de vols en masse
- Interface d'**administration Django** complète

---

## Déploiement rapide

### VM2 — Base de données
```bash
sudo apt install -y mariadb-server
# Modifier bind-address = 0.0.0.0 dans /etc/mysql/mariadb.conf.d/50-server.cnf
sudo systemctl restart mariadb
sudo mysql -u root < deploy/mariadb.sql
```

### VM1 — Serveur web
```bash
sudo apt install -y python3-venv python3-pip nginx default-libmysqlclient-dev git
git clone https://github.com/S-Adam68/sae-trafic-aerien.git
cd sae-trafic-aerien/SAE_Trafic_Aerien
python3 -m venv env && source env/bin/activate
pip install django gunicorn mysqlclient pillow
echo "STATIC_ROOT = BASE_DIR / 'staticfiles'" >> trafic_aerien/settings.py
mkdir -p static media
DB_ENGINE=mysql DB_HOST=<IP_VM2> DB_NAME=trafic_aerien_db DB_USER=trafic_user DB_PASSWORD=<mdp> python manage.py migrate
DB_ENGINE=mysql DB_HOST=<IP_VM2> DB_NAME=trafic_aerien_db DB_USER=trafic_user DB_PASSWORD=<mdp> python manage.py collectstatic --noinput
# Copier deploy/nginx.conf -> /etc/nginx/sites-available/trafic (adapter IP)
# Copier deploy/gunicorn.service -> /etc/systemd/system/gunicorn.service (adapter IP/mdp)
sudo systemctl enable --now nginx gunicorn
```

---

## Stack technique

- Python 3 / Django 6.0.5
- MariaDB (utf8mb4)
- Nginx + Gunicorn
- Bootstrap 5.3
