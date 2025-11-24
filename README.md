# 🌡️ Simulateur IoT - Capteurs Intelligents

![IoT](https://img.shields.io/badge/IoT-Simulator-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![MQTT](https://img.shields.io/badge/MQTT-Protocol-orange)
![Flask](https://img.shields.io/badge/Flask-Web-red)

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Contexte du projet](#-contexte-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Documentation technique](#-documentation-technique)
- [Exigences satisfaites](#-exigences-satisfaites)
- [Extensions réalisées](#-extensions-réalisées)
- [Dépannage](#-dépannage)

---

## 🎯 Vue d'ensemble

Ce projet est un **simulateur de capteurs IoT** complet qui reproduit le comportement de capteurs physiques et implémente une architecture IoT réelle avec communication MQTT. Le système génère des données réalistes de température, humidité et position GPS, les publie vers un broker MQTT, et offre une interface web interactive pour la visualisation et le contrôle en temps réel.

### Démonstration rapide

```bash
# Démarrer le broker MQTT
docker-compose up -d mosquitto

# Lancer l'interface web
python app.py
```

Accédez à `http://localhost:5000` pour contrôler les capteurs en temps réel ! 🚀

---

## 📝 Contexte du projet

Ce projet a été développé en réponse aux exigences suivantes :

### Objectif général
Développer un simulateur de capteurs IoT capable de :
- ✅ Générer périodiquement des données réalistes (température, humidité, position GPS)
- ✅ Les publier automatiquement vers un broker MQTT en utilisant un format JSON structuré
- ✅ Créer une interface web (Flask) permettant de visualiser en temps réel les données reçues
- ✅ Reproduire les concepts d'un système IoT réel avec l'architecture : **capteurs → broker MQTT → consommateur**

### Capteurs implémentés

#### 🌡️ Capteur de température
- Valeur centrale configurable (défaut : 22°C)
- Application d'un bruit gaussien aléatoire pour simuler un capteur réel
- Amplitude du bruit paramétrable

#### 💧 Capteur d'humidité
- Valeurs comprises entre 20% et 80%
- Variation lente dans le temps simulant des conditions réelles
- Changements progressifs pour reproduire l'inertie naturelle

#### 📍 Capteur GPS
- Position initiale (latitude/longitude) configurable
- Déplacement aléatoire simulé (quelques mètres par itération)
- Génération de trajectoires réalistes

---

## ✨ Fonctionnalités

### Simulation de capteurs
- 🔄 Génération périodique de données avec intervalle configurable (0.1s - 60s)
- 📊 Données JSON structurées avec timestamp UTC ISO8601
- 🎯 Paramètres personnalisables pour chaque capteur
- 🔌 Activation/désactivation individuelle des capteurs

### Communication MQTT
- 🌐 Connexion automatique au broker MQTT
- 🔁 Reconnexion automatique en cas de déconnexion
- 📡 Publication sur topics dédiés :
  - `iot/sensor/temperature`
  - `iot/sensor/humidity`
  - `iot/sensor/gps`
- ⚙️ Support QoS configurable
- 🛡️ Gestion robuste des erreurs

### Interface Web (Flask)
- 🎨 **Page d'accueil** : Navigation intuitive
- 🎮 **Panneau de contrôle** : Configuration des capteurs en temps réel
- 📊 **Dashboard** : Visualisation temps réel avec graphiques animés
- 📱 **QR Code** : Accès mobile via scan
- 🔌 **WebSocket** : Mise à jour instantanée des données
- 📈 **Graphiques interactifs** : Chart.js pour visualisation élégante

### Fonctionnalités avancées
- 🐳 **Docker support** : Déploiement conteneurisé
- 🔄 **Sessions** : Gestion de sessions avec ID unique
- 📱 **Responsive** : Interface adaptative mobile/desktop
- 🎨 **UI moderne** : Design épuré avec Tailwind CSS
- ⚡ **Performance** : Communication asynchrone optimisée

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Interface Web Flask                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Contrôles  │  │  Dashboard   │  │  QR Scanner  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                           │                                  │
│                    WebSocket (temps réel)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────▼───────────┐
                │   app.py (Flask)      │
                │   - Routes API        │
                │   - WebSocket server  │
                │   - Gestion sessions  │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ┌───▼────┐      ┌──────▼──────┐      ┌────▼────┐
    │ 🌡️ Temp│      │  💧 Humidity│      │ 📍 GPS  │
    │ Sensor │      │   Sensor    │      │ Sensor  │
    └────┬───┘      └──────┬──────┘      └────┬────┘
         │                 │                   │
         └─────────────────┼───────────────────┘
                           │
                  ┌────────▼─────────┐
                  │  mqtt_client.py  │
                  │  - Connexion     │
                  │  - Publication   │
                  │  - Reconnexion   │
                  └────────┬─────────┘
                           │
                           │ MQTT Protocol
                           │ (Topics: iot/sensor/*)
                           │
                  ┌────────▼─────────┐
                  │  Mosquitto Broker│
                  │  (Port 1883)     │
                  └──────────────────┘
```

### Flux de données

1. **Génération** : Les capteurs (`sensors.py`) génèrent des données JSON
2. **Publication** : Le client MQTT (`mqtt_client.py`) publie sur le broker
3. **Distribution** : Le broker Mosquitto distribue aux abonnés
4. **Visualisation** : L'interface web reçoit et affiche les données via WebSocket

---

## 🔧 Prérequis

### Logiciels requis

- **Python** 3.8 ou supérieur
- **Docker** et **Docker Compose** (recommandé pour le broker MQTT)
- **Navigateur web** moderne (Chrome, Firefox, Edge)

### Connaissances recommandées

- Python orienté objet (POO)
- Protocole MQTT
- Flask et WebSocket
- Docker (optionnel)

---

## 📦 Installation

### 1. Cloner le projet

```bash
git clone <repository-url>
cd proj-ds
```

### 2. Créer un environnement virtuel

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Démarrer le broker MQTT

#### Option A : Avec Docker (recommandé)

```bash
docker-compose up -d mosquitto
```

#### Option B : Installation locale

**Windows :**
```powershell
# Télécharger depuis https://mosquitto.org/download/
# Installer et démarrer le service
net start mosquitto
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

**Mac :**
```bash
brew install mosquitto
brew services start mosquitto
```

### 5. Vérifier l'installation

```bash
# Vérifier que Python est installé
python --version

# Vérifier les dépendances
pip list

# Tester la connexion MQTT
mosquitto_sub -h localhost -t test/#
```

---

## 🚀 Utilisation

### Démarrage rapide

#### 1. Lancer l'interface web

```bash
python app.py
```

L'application démarre sur `http://localhost:5000`

#### 2. Accéder à l'interface

- **Page d'accueil** : `http://localhost:5000/`
- **Panneau de contrôle** : `http://localhost:5000/control`
- **Dashboard** : `http://localhost:5000/dashboard`
- **Scanner QR** : `http://localhost:5000/scanner`

### Configuration des capteurs

#### Via l'interface web (Recommandé)

1. Ouvrez `http://localhost:5000/control`
2. Configurez les paramètres de chaque capteur
3. Démarrez la simulation avec le bouton "Start"
4. Visualisez les données sur le dashboard

#### Via variables d'environnement

```bash
# Configuration du broker MQTT
export BROKER_HOST=localhost
export BROKER_PORT=1883

# Configuration de Flask
export HOST=0.0.0.0
export PORT=5000

python app.py
```

### Utilisation avancée

#### Modifier l'intervalle de publication

```python
# Dans l'interface web : Slider d'intervalle (0.1s - 60s)
# Ou via API :
curl -X POST http://localhost:5000/api/update_interval \
  -H "Content-Type: application/json" \
  -d '{"interval": 2.0}'
```

#### Personnaliser un capteur

```python
# Exemple : Modifier la température de base
curl -X POST http://localhost:5000/api/update_sensor \
  -H "Content-Type: application/json" \
  -d '{
    "sensor": "temperature",
    "params": {
      "base_temp": 25.0,
      "noise_range": 3.0
    }
  }'
```

#### Accès mobile via QR Code

1. Ouvrez `http://localhost:5000/scanner`
2. Scannez le QR code affiché
3. Accédez au dashboard sur votre mobile
4. Les données s'affichent en temps réel

---

## 📁 Structure du projet

```
proj-ds/
├── app.py                      # ⭐ Application Flask principale
│   ├── Routes API REST
│   ├── Gestion WebSocket
│   ├── Contrôle simulation
│   └── Génération QR codes
│
├── sensors.py                  # ⭐ Classes de capteurs (POO)
│   ├── TemperatureSensor
│   ├── HumiditySensor
│   └── GPSSensor
│
├── mqtt_client.py              # ⭐ Client MQTT
│   ├── Connexion broker
│   ├── Publication JSON
│   ├── Reconnexion auto
│   └── Gestion erreurs
│
├── templates/                  # 🎨 Templates HTML
│   ├── index.html             # Page d'accueil
│   ├── control.html           # Panneau de contrôle
│   ├── dashboard.html         # Visualisation temps réel
│   └── scanner.html           # Scanner QR code
│
├── mosquitto/                  # 🦟 Configuration Mosquitto
│   ├── config/
│   │   └── mosquitto.conf     # Configuration broker
│   ├── data/                  # Persistance données
│   └── log/                   # Logs broker
│
├── requirements.txt            # 📦 Dépendances Python
├── Dockerfile                  # 🐳 Image Docker
├── docker-compose.yml          # 🐳 Orchestration services
├── supervisord.conf            # ⚙️ Gestion processus
└── README.md                   # 📖 Documentation (ce fichier)
```

### Modules principaux

#### `sensors.py` - Capteurs IoT

```python
# Architecture POO avec classes dédiées
TemperatureSensor(base_temp=22.0, noise_range=2.0)
HumiditySensor(initial_humidity=55.0)
GPSSensor(initial_lat=48.8566, initial_lon=2.3522)

# Méthode commune : read()
data = sensor.read()
# Retourne : {
#   "timestamp": "2025-11-24T10:30:45.123456+00:00",
#   "sensor": "temperature",
#   "value": 23.47,
#   "unit": "°C"
# }
```

#### `mqtt_client.py` - Communication MQTT

```python
# Encapsulation complète du protocole MQTT
client = MQTTClient(
    broker_host="localhost",
    broker_port=1883,
    client_id="iot_sim_12345"
)

client.connect()
client.publish(topic="iot/sensor/temp", data=sensor_data, qos=1)
client.disconnect()
```

#### `app.py` - Interface Web

```python
# API REST + WebSocket + Dashboard
# Routes principales :
@app.route('/api/start')        # Démarrer simulation
@app.route('/api/stop')         # Arrêter simulation
@app.route('/api/status')       # État du système
@socketio.on('connect')         # WebSocket temps réel
```

---

## 📚 Documentation technique

### Format des données JSON

#### Température

```json
{
  "timestamp": "2025-11-24T10:30:45.123456+00:00",
  "sensor": "temperature",
  "value": 23.47,
  "unit": "°C"
}
```

#### Humidité

```json
{
  "timestamp": "2025-11-24T10:30:45.123456+00:00",
  "sensor": "humidity",
  "value": 58.32,
  "unit": "%"
}
```

#### GPS

```json
{
  "timestamp": "2025-11-24T10:30:45.123456+00:00",
  "sensor": "gps",
  "lat": 48.856789,
  "lon": 2.352345,
  "unit": "degrees"
}
```

### Topics MQTT

| Topic | Description | QoS | Retained |
|-------|-------------|-----|----------|
| `iot/sensor/temperature` | Données de température | 1 | Non |
| `iot/sensor/humidity` | Données d'humidité | 1 | Non |
| `iot/sensor/gps` | Position GPS | 1 | Non |

### API REST

#### GET `/api/status`
Retourne l'état actuel du simulateur.

**Réponse :**
```json
{
  "running": true,
  "interval": 1.0,
  "session_id": "abc123-def456",
  "sensors": {
    "temperature": {
      "base_temp": 22.0,
      "noise_range": 2.5,
      "enabled": true
    },
    ...
  }
}
```

#### POST `/api/start`
Démarre la simulation.

**Réponse :**
```json
{
  "status": "success",
  "message": "Simulation démarrée"
}
```

#### POST `/api/stop`
Arrête la simulation.

#### POST `/api/update_sensor`
Met à jour les paramètres d'un capteur.

**Requête :**
```json
{
  "sensor": "temperature",
  "params": {
    "base_temp": 25.0,
    "noise_range": 3.0
  }
}
```

#### POST `/api/update_interval`
Modifie l'intervalle de publication (0.1s - 60s).

**Requête :**
```json
{
  "interval": 2.0
}
```

### WebSocket Events

#### Client → Server
- `connect` : Connexion établie
- `disconnect` : Déconnexion

#### Server → Client
- `status` : État du simulateur
- `sensor_data` : Nouvelles données capteur

**Format `sensor_data` :**
```json
{
  "sensor": "temperature",
  "data": {
    "timestamp": "...",
    "value": 23.47,
    ...
  }
}
```

---

## ✅ Exigences satisfaites

### Contraintes techniques obligatoires

| Exigence | Statut | Implémentation |
|----------|--------|----------------|
| Architecture modulaire (3+ modules) | ✅ | `sensors.py`, `mqtt_client.py`, `app.py` |
| POO pour les capteurs | ✅ | Classes `TemperatureSensor`, `HumiditySensor`, `GPSSensor` |
| Format JSON | ✅ | Sérialisation JSON pour tous les messages |
| Connexion MQTT avec `paho-mqtt` | ✅ | Module `mqtt_client.py` |
| Code documenté | ✅ | Docstrings et commentaires exhaustifs |
| Protocole MQTT (topics, QoS) | ✅ | Topics dédiés, QoS=1 |
| Génération de données réalistes | ✅ | Bruit gaussien, variations progressives |
| Timestamp UTC ISO8601 | ✅ | `datetime.now(timezone.utc).isoformat()` |
| Intervalle configurable | ✅ | 0.1s à 60s via API ou interface |
| Reconnexion automatique | ✅ | Gestion dans `MQTTClient` |
| Arrêt propre (Ctrl+C) | ✅ | Gestion des signaux |
| Affichage console | ✅ | Logging structuré |

### Capteurs implémentés

| Capteur | Statut | Caractéristiques |
|---------|--------|------------------|
| 🌡️ Température | ✅ | Valeur centrale + bruit gaussien configurable |
| 💧 Humidité | ✅ | Variation lente 20-80%, simulation inertie |
| 📍 GPS | ✅ | Position initiale + déplacement aléatoire |

---

## 🎁 Extensions réalisées

### Interface Web Flask (Optionnelle → ✅ Réalisée)

#### Fonctionnalités principales
- ✅ **Dashboard temps réel** avec WebSocket
- ✅ **Panneau de contrôle** interactif
- ✅ **Graphiques animés** (Chart.js)
- ✅ **Scanner QR Code** pour accès mobile
- ✅ **API REST complète**
- ✅ **Design responsive** (Tailwind CSS)

#### Fonctionnalités bonus
- 🎨 Interface utilisateur moderne et intuitive
- 📱 Support mobile complet
- 🔄 Mise à jour temps réel sans rechargement
- 📊 Visualisation graphique des données
- ⚙️ Configuration dynamique des capteurs
- 🔐 Gestion de sessions avec ID unique
- 📷 Génération QR codes pour accès rapide

### Docker & Déploiement

- ✅ `Dockerfile` pour conteneurisation
- ✅ `docker-compose.yml` pour orchestration
- ✅ Configuration Mosquitto personnalisée
- ✅ Supervisord pour gestion multi-processus

### Qualité du code

- ✅ Type hints Python
- ✅ Logging structuré
- ✅ Gestion d'erreurs robuste
- ✅ Documentation exhaustive
- ✅ Architecture MVC claire

---

## 🐛 Dépannage

### Problèmes courants

#### ❌ Erreur : "Connection refused" (MQTT)

**Cause :** Le broker Mosquitto n'est pas démarré.

**Solution :**
```bash
# Vérifier le statut
docker-compose ps

# Démarrer le broker
docker-compose up -d mosquitto

# Vérifier les logs
docker-compose logs mosquitto
```

#### ❌ Erreur : "Address already in use" (Port 5000)

**Cause :** Un autre processus utilise le port 5000.

**Solution :**
```bash
# Trouver le processus
netstat -ano | findstr :5000

# Arrêter le processus ou changer le port
$env:PORT=5001
python app.py
```

#### ❌ Les graphiques ne s'affichent pas

**Cause :** Connexion WebSocket échouée.

**Solution :**
1. Vérifier la console navigateur (F12)
2. Vérifier que Flask-SocketIO est installé
3. Recharger la page

#### ❌ Données GPS incohérentes

**Cause :** Cumul d'erreurs d'arrondi.

**Solution :**
```python
# Réinitialiser la position GPS
curl -X POST http://localhost:5000/api/update_sensor \
  -H "Content-Type: application/json" \
  -d '{
    "sensor": "gps",
    "params": {
      "lat": 48.8566,
      "lon": 2.3522
    }
  }'
```

### Logs et débogage

#### Activer le mode debug Flask

```bash
# Dans app.py, modifier la dernière ligne :
socketio.run(app, host=host, port=port, debug=True)
```

#### Consulter les logs MQTT

```bash
# Logs du broker
docker-compose logs -f mosquitto

# Logs de l'application
# Visibles directement dans le terminal où app.py est lancé
```

#### Tester la connexion MQTT manuellement

```bash
# S'abonner à tous les topics
mosquitto_sub -h localhost -t "iot/sensor/#" -v

# Publier un message test
mosquitto_pub -h localhost -t "iot/sensor/test" -m '{"test": true}'
```

---

## 🤝 Contribution

Ce projet est un travail académique. Pour toute suggestion ou amélioration :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est développé dans un cadre éducatif.

---

## 👤 Auteur

**Seif**
- GitHub: [@seif2003](https://github.com/seif2003)
- Repository: [Simulateur-IoT](https://github.com/seif2003/Simulateur-IoT)

---

## 🙏 Remerciements

- **Eclipse Mosquitto** pour le broker MQTT open-source
- **Flask** et **Flask-SocketIO** pour le framework web
- **Paho MQTT** pour la bibliothèque Python
- **Chart.js** pour les graphiques interactifs
- **Tailwind CSS** pour le design moderne

---

## 📞 Support

Pour toute question ou problème :

1. Vérifier la section [Dépannage](#-dépannage)
2. Consulter les logs de l'application
3. Ouvrir une issue sur GitHub

---

**Dernière mise à jour :** Novembre 2025  
**Version :** 1.0.0  
**Statut :** ✅ Production Ready
