# Guide de Déploiement Docker - Simulateur IoT

## 🎯 Vue d'ensemble

Ce guide explique comment déployer le simulateur IoT avec Docker sur différents environnements.

## 📦 Contenu Docker

### Images Docker
- **Flask App** : Application web Python avec SocketIO
- **Mosquitto** : Broker MQTT Eclipse Mosquitto

### Réseau Docker
- Réseau privé `iot_network` pour communication inter-conteneurs
- Ports exposés : 5000 (web), 1883 (MQTT), 9001 (MQTT WebSocket)

## 🚀 Démarrage Rapide

### Développement Local
```bash
# Cloner le projet
git clone https://github.com/seif2003/Simulateur-IoT.git
cd Simulateur-IoT

# Démarrer
docker-compose up --build

# Accès : http://localhost:5000
```

### Production
```bash
# Utiliser la config production (port 80)
docker-compose -f docker-compose.prod.yml up --build -d

# Accès : http://your-server-ip
```

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env` :
```env
# MQTT Broker
BROKER_HOST=mosquitto
BROKER_PORT=1883

# Flask App
HOST=0.0.0.0
PORT=5000
```

### Modifier l'URL du QR Code

Pour production, éditer `app.py` ligne ~185 :
```python
# Development
dashboard_url = f"http://localhost:5000/dashboard/{session_id}"

# Production - remplacer par votre domaine
dashboard_url = f"http://your-domain.com/dashboard/{session_id}"
```

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│            Docker Host                      │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │   Container: mosquitto             │    │
│  │   - MQTT Broker                    │    │
│  │   - Ports: 1883, 9001             │    │
│  └─────────────┬──────────────────────┘    │
│                │                            │
│  ┌─────────────▼──────────────────────┐    │
│  │   Container: web                   │    │
│  │   - Flask + SocketIO               │    │
│  │   - Port: 5000                     │    │
│  │   - Environment: BROKER_HOST=mqtt  │    │
│  └────────────────────────────────────┘    │
│                                             │
└─────────────────────────────────────────────┘
         ▲                      ▲
         │                      │
    Port 1883              Port 5000
    (MQTT)                (Web UI)
```

## 🔍 Commandes Utiles

### État des Conteneurs
```bash
docker-compose ps
docker-compose top
docker stats
```

### Logs
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f web
docker-compose logs -f mosquitto

# Sauvegarder les logs
docker-compose logs > logs.txt
```

### Gestion des Volumes
```bash
# Lister les volumes
docker volume ls

# Inspecter un volume
docker volume inspect proj-ds_mosquitto_data

# Nettoyer les volumes orphelins
docker volume prune
```

### Rebuild
```bash
# Rebuild sans cache
docker-compose build --no-cache

# Rebuild et redémarrer
docker-compose up --build -d
```

### Accès Shell
```bash
# Shell dans le conteneur web
docker-compose exec web bash

# Shell dans mosquitto
docker-compose exec mosquitto sh

# Exécuter une commande Python
docker-compose exec web python -c "import sensors; print('OK')"
```

## 🌐 Déploiement Cloud

### DigitalOcean / AWS / Azure

**1. Créer une VM avec Docker installé**

**2. Cloner et configurer**
```bash
git clone https://github.com/seif2003/Simulateur-IoT.git
cd Simulateur-IoT
cp .env.example .env
```

**3. Modifier l'URL dans app.py**
```python
# Utiliser l'IP publique ou le domaine
dashboard_url = f"http://YOUR_PUBLIC_IP:5000/dashboard/{session_id}"
```

**4. Démarrer**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**5. Configurer le pare-feu**
```bash
# UFW (Ubuntu)
sudo ufw allow 80/tcp
sudo ufw allow 1883/tcp
sudo ufw enable
```

### Avec Nginx Reverse Proxy

**docker-compose.nginx.yml**
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - web
    networks:
      - iot_network

  # ... reste de la configuration
```

## 🔒 Sécurité Production

### 1. Authentification MQTT

Modifier `mosquitto/config/mosquitto.conf` :
```conf
allow_anonymous false
password_file /mosquitto/config/passwd
```

Créer le fichier de mots de passe :
```bash
docker-compose exec mosquitto mosquitto_passwd -c /mosquitto/config/passwd iot_user
```

### 2. HTTPS avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot

# Obtenir certificat
sudo certbot certonly --standalone -d your-domain.com

# Configurer Nginx pour HTTPS (voir README.md)
```

### 3. Firewall
```bash
# Autoriser uniquement les ports nécessaires
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 1883/tcp
sudo ufw enable
```

## 📈 Monitoring

### Logs centralisés
```bash
# Installer Loki + Promtail (optionnel)
docker run -d --name=loki grafana/loki:latest
```

### Métriques
```bash
# Docker stats en temps réel
watch -n 1 docker stats --no-stream
```

## 🔄 Mise à jour

```bash
# Pull les dernières modifications
git pull

# Rebuild et redémarrer
docker-compose down
docker-compose up --build -d

# Vérifier
docker-compose ps
docker-compose logs -f
```

## 🆘 Dépannage

### Le conteneur web ne démarre pas
```bash
# Voir les logs détaillés
docker-compose logs web

# Vérifier les dépendances
docker-compose exec web pip list

# Rebuild complet
docker-compose down
docker-compose build --no-cache web
docker-compose up web
```

### Problème de connexion MQTT
```bash
# Tester depuis le conteneur web
docker-compose exec web ping mosquitto

# Vérifier que mosquitto écoute
docker-compose exec mosquitto netstat -tln | grep 1883

# Tester la publication
docker-compose exec mosquitto mosquitto_pub -t test -m "hello"
docker-compose exec mosquitto mosquitto_sub -t test
```

### Volumes corrompus
```bash
# Supprimer tous les volumes
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

## 📚 Ressources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Mosquitto Docker Image](https://hub.docker.com/_/eclipse-mosquitto)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

**Note** : Ce guide est pour la version dockerisée du projet. Pour le développement local sans Docker, voir README.md.
