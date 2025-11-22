# 🌐 Simulateur IoT avec Interface Web et QR Codes

Système IoT complet avec capteurs simulés, broker MQTT Mosquitto, interface web Flask et accès via QR codes pour le monitoring en temps réel.

## 📋 Vue d'Ensemble

Ce projet simule un environnement IoT avec trois types de capteurs (température, humidité, GPS) qui publient leurs données sur un broker MQTT. L'interface web permet de contrôler la simulation, visualiser les données en temps réel et partager l'accès via QR codes.

## ✨ Fonctionnalités Principales

### 📡 Capteurs Simulés
- **🌡️ Température** : Génération avec bruit gaussien réaliste (base configurable, ±2.5°C)
- **💧 Humidité** : Variation lente et progressive entre 20% et 80%
- **📍 GPS** : Simulation de déplacement avec marche aléatoire (~11 mètres par itération)

### 🎨 Interface Web Moderne
✅ **Design dark moderne** inspiré de shadcn/ui  
✅ **Couleur primaire rouge** (#e7000b) pour tous les accents  
✅ **Contrôles interactifs** avec sliders en temps réel  
✅ **Dashboard intégré** avec WebSocket pour mise à jour instantanée  
✅ **Graphiques dynamiques** (Chart.js avec historique de 50 points)  
✅ **Carte GPS interactive** (Leaflet/OpenStreetMap avec trajectoire)  
✅ **QR Code unique** pour partage de session  
✅ **Scanner QR** intégré avec accès caméra  
✅ **Génération automatique** de session ID (UUID) à chaque visite  
✅ **Responsive** et optimisé mobile

### Architecture MQTT
- Topics dédiés : `iot/sensor/temperature`, `humidity`, `gps`
- Format JSON avec timestamp UTC ISO8601
- QoS 1 pour garantie de livraison
- Reconnexion automatique

## 🚀 Installation et Démarrage

### Prérequis
- Docker & Docker Compose
- Python 3.7+
- pip

### 1️⃣ Installer les dépendances
```powershell
pip install -r requirements.txt
```

### 2️⃣ Démarrer le broker MQTT
```powershell
docker-compose up -d
```

### 3️⃣ Lancer l'interface web
```powershell
python app.py
```

### 4️⃣ Accéder à l'interface
Ouvrez : **http://localhost:5000**

## 🗂️ Architecture du Projet

### Technologies Utilisées
- **Backend** : Flask 2.3+, Flask-SocketIO 5.3+, Flask-CORS
- **MQTT** : paho-mqtt 1.6+, Mosquitto (Docker)
- **Temps Réel** : Socket.IO avec WebSocket
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
- **Visualisation** : Chart.js 4.4, Leaflet 1.9
- **QR Codes** : qrcode 7.4+, pillow 10.0+, html5-qrcode 2.3
- **Conteneurisation** : Docker Compose

### Pattern Architectural
- **OOP modulaire** : Séparation des responsabilités (capteurs, MQTT, web)
- **Pub/Sub MQTT** : Communication asynchrone via topics
- **WebSocket bidirectionnel** : Mise à jour temps réel client-serveur
- **Session Management** : UUID pour identifier chaque simulation
- **RESTful API** : Endpoints pour contrôle et configuration

## 📱 Pages de l'Interface

### 🏠 Accueil (`/`)
Page d'accueil avec navigation vers :
- **Contrôles** : Interface principale de simulation et visualisation
- **Scanner QR** : Accès aux dashboards partagés

### 🎛️ Contrôles (`/control`)
**Page principale intégrant contrôle + dashboard**

#### Section QR Code
- Génération automatique d'un **QR code unique** à chaque session
- Affichage de l'**ID de session** avec bouton de copie
- QR code mène au dashboard complet avec tous les capteurs
- **Nouvelle session** générée automatiquement à chaque rechargement

#### Contrôles de Simulation
- Boutons **Démarrer/Arrêter** la publication MQTT
- Indicateur d'état en temps réel
- Ajustement de l'**intervalle de publication** (0.1s à 10s)

#### Configuration des Capteurs
**Température**
- Toggle on/off
- Slider température de base (0-50°C)
- Affichage valeur actuelle

**Humidité**
- Toggle on/off  
- Slider humidité de base (20-80%)
- Affichage valeur actuelle

**GPS**
- Toggle on/off
- Sliders latitude et longitude (-90 à 90, -180 à 180)
- Affichage position actuelle

### 📊 Dashboard (`/dashboard/<session_id>`)
**Accès via QR code ou URL directe**

#### Statistiques en Temps Réel
- 3 cartes affichant valeurs instantanées
- Timestamps de dernière mise à jour
- Unités clairement indiquées

#### Graphiques Historiques
- **Température** : Ligne rouge avec transparence
- **Humidité** : Ligne rouge claire
- Historique des 50 dernières lectures
- Axes avec grille et labels

#### Carte GPS Interactive
- Marqueur de position actuelle
- Trajectoire en rouge (100 derniers points max)
- Pan smooth sans clignotement
- Tuiles OpenStreetMap

#### Indicateur de Connexion
- ⚫ Déconnecté / 🟢 Connecté
- Mise à jour automatique via WebSocket

### 📱 Scanner (`/scanner`)
Interface pour accéder aux dashboards partagés

**Onglet Scanner QR**
- Accès caméra HTML5
- Détection automatique des QR codes
- Redirection instantanée vers le dashboard

**Onglet Saisie Manuelle**
- Champ pour entrer l'ID de session
- Validation et redirection
- Alternative sans caméra

## 📱 Système de QR Code & Sessions

### Gestion des Sessions
- **UUID unique** généré automatiquement à chaque visite de `/control`
- Permet le partage de dashboards entre appareils
- Pas de persistance (sessions volatiles en mémoire)

### QR Code Unique
**Un seul QR code** par session menant au dashboard complet :
- Généré dynamiquement avec tous les capteurs
- URL format : `http://localhost:5000/dashboard/<session_id>`
- Image PNG 300x300px avec correction d'erreur

### Workflow de Partage
1. Ouvrir `/control` → Session ID créé automatiquement
2. QR code affiché avec le nouvel ID
3. Scanner le QR avec mobile → Accès direct au dashboard
4. **Alternative** : Copier l'ID et le saisir via `/scanner`

### Endpoints API
- `GET /api/qrcode` - Génère le QR code pour la session actuelle
- `POST /api/session/new` - Force la création d'une nouvelle session
- `GET /api/status` - Retourne l'état avec session_id

## 📊 Format des Données

### Température
```json
{
  "timestamp": "2025-11-22T10:30:45+00:00",
  "sensor": "temperature",
  "value": 23.45,
  "unit": "°C"
}
```

### Humidité
```json
{
  "timestamp": "2025-11-22T10:30:45+00:00",
  "sensor": "humidity",
  "value": 56.78,
  "unit": "%"
}
```

### GPS
```json
{
  "timestamp": "2025-11-22T10:30:45+00:00",
  "sensor": "gps",
  "lat": 48.856700,
  "lon": 2.352300,
  "unit": "degrees"
}
```

## ⚙️ Configuration

### Modifier les paramètres via l'interface
Tous les paramètres sont modifiables en temps réel via les sliders

### Modifier le broker MQTT
Dans `app.py` :
```python
BROKER_HOST = "localhost"
BROKER_PORT = 1883
```

## 🐳 Gestion Docker

```powershell
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Logs
docker-compose logs -f mosquitto

# Redémarrer
docker-compose restart
```

## 📁 Structure du Projet

```
proj-ds/
├── app.py                  # Application Flask + SocketIO + Routes
├── sensors.py              # Classes TemperatureSensor, HumiditySensor, GPSSensor
├── mqtt_client.py          # Wrapper client MQTT avec reconnexion
├── requirements.txt        # Dépendances Python
├── docker-compose.yml      # Configuration Mosquitto
├── README.md              # Documentation complète
├── .gitignore             # Fichiers à ignorer
├── templates/
│   ├── index.html         # Page d'accueil (2 cards)
│   ├── control.html       # Interface principale (contrôles + dashboard intégré)
│   ├── dashboard.html     # Dashboard standalone (accès via session_id)
│   └── scanner.html       # Scanner QR + saisie manuelle
└── mosquitto/
    ├── config/
    │   └── mosquitto.conf # Configuration broker
    ├── data/              # Persistence MQTT
    └── log/               # Logs broker
```

## 🎨 Design System

### Palette de Couleurs
- **Fond** : `#09090b` (noir profond)
- **Cartes/Panneaux** : `#18181b` (gris très foncé)
- **Bordures** : `#27272a` (gris foncé), `#3f3f46` (gris moyen)
- **Texte** : `#fafafa` (blanc cassé), `#e4e4e7` (gris clair), `#a1a1aa` (gris)
- **Primaire** : `#e7000b` (rouge vif)
- **Hover** : `#c00009` (rouge foncé)
- **Accent** : `#ff4d56` (rouge clair)
- **Succès** : `#16a34a` (vert)

### Typographie
- **Font Stack** : -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif
- **Poids** : 400 (normal), 500 (medium), 600 (semi-bold), 700 (bold)
- **Tailles** : 0.75em → 2.5em selon hiérarchie

### Composants
- **Boutons** : Radius 8px, padding 10-12px, transition 0.2s
- **Cartes** : Border 1px, radius 12px, hover avec changement de border
- **Sliders** : Thumb circulaire 18px rouge, track gris foncé
- **Toggles** : Switch 60x30px avec animation smooth

## 🔧 API REST Complète

### Routes Pages
- `GET /` - Page d'accueil
- `GET /control` - Interface de contrôle principale
- `GET /dashboard` - Dashboard sans session (redirection)
- `GET /dashboard/<session_id>` - Dashboard avec session spécifique
- `GET /scanner` - Page scanner QR

### Endpoints API
| Méthode | Endpoint | Description | Payload |
|---------|----------|-------------|---------|
| GET | `/api/status` | État du simulateur + session_id | - |
| POST | `/api/start` | Démarrer la simulation | - |
| POST | `/api/stop` | Arrêter la simulation | - |
| POST | `/api/update_sensor` | Modifier paramètres capteur | `{sensor, params}` |
| POST | `/api/update_interval` | Changer intervalle publication | `{interval}` |
| GET | `/api/qrcode` | Générer QR code session actuelle | - |
| POST | `/api/session/new` | Créer nouvelle session UUID | - |

### Exemples de Requêtes

**Démarrer la simulation**
```javascript
fetch('/api/start', { method: 'POST' })
```

**Modifier la température de base**
```javascript
fetch('/api/update_sensor', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sensor: 'temperature',
    params: { base_temp: 25.0 }
  })
})
```

**Activer/désactiver un capteur**
```javascript
fetch('/api/update_sensor', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    sensor: 'humidity',
    params: { enabled: false }
  })
})
```

## 🔌 Communication WebSocket

### Événements Socket.IO

**Côté Serveur → Client**
- `sensor_data` : Émis à chaque lecture de capteur
  ```javascript
  {
    sensor: 'temperature',  // ou 'humidity', 'gps'
    data: { value: 23.5, timestamp: '...', unit: '°C' }
  }
  ```

**Connexion**
- `connect` : Connexion établie
- `disconnect` : Connexion perdue

### Gestion Temps Réel
- Mode `async_mode='threading'` pour Flask-SocketIO
- Émission broadcast pour tous les clients connectés
- Pas de rooms (tous reçoivent toutes les données)
- Reconnexion automatique côté client

## 🎯 Cas d'Usage

### Monitoring Mobile
1. Lancer la simulation sur PC (`python app.py`)
2. Ouvrir `/control` pour générer le QR code
3. Scanner le QR avec smartphone
4. Dashboard accessible instantanément sur mobile
5. Données synchronisées en temps réel

### Partage de Session
1. Copier l'ID de session affiché sur `/control`
2. Partager l'ID par message/email
3. Destinataire accède via `/scanner`
4. Saisir l'ID manuellement
5. Tous les utilisateurs voient les mêmes données live

### Démonstration/Présentation
1. Projeter `/control` pour montrer les contrôles
2. QR code visible au public
3. Participants scannent et suivent sur leurs appareils
4. Ajustements en direct visibles par tous

### Développement/Test IoT
1. Tester l'intégration MQTT sans capteurs physiques
2. Simuler différents scénarios (températures extrêmes, déplacements GPS)
3. Valider le comportement de l'application consommatrice
4. Déboguer la visualisation temps réel

## 🛠️ Détails Techniques

### Classes Capteurs (`sensors.py`)

**TemperatureSensor**
- `base_temp` : Température de référence (défaut 22°C)
- `noise_range` : Amplitude du bruit (±2.5°C)
- Génération avec `random.gauss()` pour réalisme

**HumiditySensor**
- `base_humidity` : Humidité de référence (défaut 50%)
- Variation lente : ±2% par lecture
- Clamping entre 20% et 80%

**GPSSensor**
- `lat`, `lon` : Position de départ
- Déplacement aléatoire : ±0.0001° (~11m)
- Utilise `math.cos()` et `math.sin()` pour direction

### Client MQTT (`mqtt_client.py`)
- **Reconnexion automatique** avec retry
- **QoS 1** : Garantie de livraison au moins une fois
- **Clean session** : False pour persistence
- Callbacks : `_on_connect`, `_on_disconnect`, `_on_publish`
- Logger intégré pour debugging

### Application Flask (`app.py`)
- **Thread séparé** pour simulation (évite blocage)
- **État global** `simulator_state` (running, interval, sensors, session_id)
- **CORS activé** pour développement
- **SocketIO** avec mode threading
- Initialisation MQTT au démarrage

## ⚙️ Configuration Mosquitto

Fichier `mosquitto/config/mosquitto.conf` :
```conf
listener 1883
listener 9001
protocol websockets
allow_anonymous true
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
```

- Port **1883** : MQTT classique
- Port **9001** : WebSocket (pour navigateurs)
- Anonymous activé (dev uniquement)
- Persistence des messages

## 🐛 Troubleshooting

### Le serveur Flask ne démarre pas
```powershell
# Vérifier les dépendances
pip install -r requirements.txt

# Vérifier le port 5000
netstat -ano | findstr :5000
```

### Mosquitto ne démarre pas
```powershell
# Vérifier Docker
docker ps

# Logs Mosquitto
docker-compose logs mosquitto

# Recréer les volumes
docker-compose down -v
docker-compose up -d
```

### Dashboard ne reçoit pas de données
1. Vérifier que la simulation est **démarrée** (bouton vert)
2. Vérifier connexion WebSocket (🟢 Connecté)
3. Ouvrir console navigateur (F12) pour erreurs
4. Vérifier que Mosquitto tourne : `docker ps`

### QR Code ne fonctionne pas
1. Vérifier que `qrcode` et `pillow` sont installés
2. Vérifier URL dans le QR : doit contenir `session_id`
3. S'assurer que le mobile peut accéder à `localhost:5000` (même réseau ou ngrok)

## 🔐 Sécurité & Limitations

### ⚠️ Version Développement
Ce projet est conçu pour l'apprentissage et le développement. **Ne pas utiliser en production** sans :

- ✅ **Authentification MQTT** (username/password)
- ✅ **TLS/SSL** sur MQTT et Flask
- ✅ **HTTPS** pour l'interface web
- ✅ **Rate limiting** sur les API
- ✅ **Validation des entrées** utilisateur
- ✅ **Expiration des sessions** (TTL)
- ✅ **CORS restrictif** (whitelist domains)
- ✅ **Sanitization** des données MQTT

### Limitations Actuelles
- Sessions en mémoire (perdues au redémarrage)
- Pas d'authentification utilisateur
- Un seul simulateur par instance
- Pas de persistence historique
- Allow anonymous sur MQTT

## 📚 Ressources & Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [Mosquitto MQTT](https://mosquitto.org/documentation/)
- [Chart.js](https://www.chartjs.org/docs/)
- [Leaflet Maps](https://leafletjs.com/reference.html)
- [paho-mqtt Python](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)

## 📄 Licence

Projet académique - Université  
Libre d'utilisation pour l'éducation et l'apprentissage

---

**Stack Technique** : Python, Flask, Socket.IO, MQTT/Mosquitto, Chart.js, Leaflet, Docker  
**Design** : Dark theme moderne inspiré de shadcn/ui avec accent rouge  
**Auteur** : Projet IoT - 2025
