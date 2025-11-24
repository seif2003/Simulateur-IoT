"""
Application Flask pour l'interface web du simulateur IoT.
Fournit un dashboard en temps réel et des contrôles pour les capteurs.
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import threading
import time
import logging
import uuid
import qrcode
from io import BytesIO
from sensors import TemperatureSensor, HumiditySensor, GPSSensor
from mqtt_client import MQTTClient

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialisation Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'iot_simulator_secret_2025'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# État global du simulateur
simulator_state = {
    'running': False,
    'interval': 1.0,
    'session_id': str(uuid.uuid4()),  # ID unique de session
    'sensors': {
        'temperature': {
            'base_temp': 22.0,
            'noise_range': 2.5,
            'enabled': True
        },
        'humidity': {
            'initial_humidity': 55.0,
            'enabled': True
        },
        'gps': {
            'lat': 48.8566,
            'lon': 2.3522,
            'enabled': True
        }
    }
}

# Instances des capteurs et client MQTT
sensors = {}
mqtt_client = None
simulation_thread = None


def init_sensors():
    """Initialise les capteurs avec les paramètres actuels."""
    global sensors
    
    config = simulator_state['sensors']
    sensors = {
        'temperature': TemperatureSensor(
            base_temp=config['temperature']['base_temp'],
            noise_range=config['temperature']['noise_range']
        ),
        'humidity': HumiditySensor(
            initial_humidity=config['humidity']['initial_humidity']
        ),
        'gps': GPSSensor(
            initial_lat=config['gps']['lat'],
            initial_lon=config['gps']['lon']
        )
    }


def init_mqtt():
    """Initialise le client MQTT."""
    global mqtt_client
    
    import os
    broker_host = os.getenv('BROKER_HOST', 'localhost')
    broker_port = int(os.getenv('BROKER_PORT', '1883'))
    
    mqtt_client = MQTTClient(
        broker_host=broker_host,
        broker_port=broker_port,
        client_id="iot_simulator_web"
    )
    
    if mqtt_client.connect(timeout=10):
        logger.info(f"✓ Connecté au broker MQTT ({broker_host}:{broker_port})")
        return True
    else:
        logger.error(f"✗ Échec de connexion au broker MQTT ({broker_host}:{broker_port})")
        return False


def simulation_loop():
    """Boucle de simulation qui s'exécute dans un thread séparé."""
    global simulator_state
    
    logger.info("Thread de simulation démarré")
    
    topics = {
        'temperature': 'iot/sensor/temperature',
        'humidity': 'iot/sensor/humidity',
        'gps': 'iot/sensor/gps'
    }
    
    while simulator_state['running']:
        try:
            # Lire et publier chaque capteur activé
            for sensor_name, sensor in sensors.items():
                if simulator_state['sensors'][sensor_name]['enabled']:
                    data = sensor.read()
                    
                    # Publier sur MQTT
                    if mqtt_client and mqtt_client.is_connected():
                        mqtt_client.publish(topics[sensor_name], data, qos=1)
                    
                    # Envoyer via WebSocket pour le dashboard
                    socketio.emit('sensor_data', {
                        'sensor': sensor_name,
                        'data': data
                    })
            
            time.sleep(simulator_state['interval'])
            
        except Exception as e:
            logger.error(f"Erreur dans la boucle de simulation: {e}")
    
    logger.info("Thread de simulation arrêté")


@app.route('/')
def index():
    """Page d'accueil avec liens vers contrôles et dashboard."""
    return render_template('index.html')


@app.route('/control')
def control():
    """Page de contrôle des capteurs."""
    return render_template('control.html')


@app.route('/scanner')
def scanner():
    """Page de scan QR code."""
    return render_template('scanner.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard de visualisation en temps réel."""
    return render_template('dashboard.html')


@app.route('/dashboard/<session_id>')
def dashboard_with_session(session_id):
    """Dashboard avec ID de session spécifique."""
    if session_id == simulator_state['session_id']:
        return render_template('dashboard.html', session_id=session_id)
    else:
        return render_template('dashboard.html', error='Session invalide')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Retourne l'état actuel du simulateur."""
    return jsonify(simulator_state)


@app.route('/api/qrcode')
def generate_qrcode():
    """Génère un QR code pour accéder au dashboard complet."""
    session_id = simulator_state['session_id']
    
    # URL vers le dashboard complet avec session ID
    base_url = request.host_url.rstrip('/')
    dashboard_url = f"{base_url}/dashboard/{session_id}"
    
    # Générer le QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(dashboard_url)
    qr.make(fit=True)
    
    # Créer l'image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir en bytes
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')


@app.route('/api/session/new', methods=['POST'])
def new_session():
    """Crée une nouvelle session et retourne le nouvel ID."""
    simulator_state['session_id'] = str(uuid.uuid4())
    logger.info(f"Nouvelle session créée: {simulator_state['session_id']}")
    return jsonify({
        'status': 'success',
        'session_id': simulator_state['session_id']
    })


@app.route('/api/start', methods=['POST'])
def start_simulation():
    """Démarre la simulation."""
    global simulation_thread, simulator_state
    
    if simulator_state['running']:
        return jsonify({'status': 'error', 'message': 'Simulation déjà en cours'})
    
    # Initialiser les capteurs et MQTT
    init_sensors()
    if not init_mqtt():
        return jsonify({'status': 'error', 'message': 'Impossible de se connecter au broker MQTT'})
    
    # Démarrer le thread de simulation
    simulator_state['running'] = True
    simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
    simulation_thread.start()
    
    logger.info("✓ Simulation démarrée")
    return jsonify({'status': 'success', 'message': 'Simulation démarrée'})


@app.route('/api/stop', methods=['POST'])
def stop_simulation():
    """Arrête la simulation."""
    global simulator_state, mqtt_client
    
    if not simulator_state['running']:
        return jsonify({'status': 'error', 'message': 'Simulation non active'})
    
    simulator_state['running'] = False
    
    if mqtt_client:
        mqtt_client.disconnect()
    
    logger.info("✓ Simulation arrêtée")
    return jsonify({'status': 'success', 'message': 'Simulation arrêtée'})


@app.route('/api/update_sensor', methods=['POST'])
def update_sensor():
    """Met à jour les paramètres d'un capteur."""
    data = request.json
    sensor_type = data.get('sensor')
    params = data.get('params')
    
    if sensor_type not in simulator_state['sensors']:
        return jsonify({'status': 'error', 'message': 'Capteur inconnu'})
    
    # Mettre à jour les paramètres
    simulator_state['sensors'][sensor_type].update(params)
    
    # Si la simulation est active, recréer le capteur
    if simulator_state['running'] and sensor_type in sensors:
        if sensor_type == 'temperature':
            sensors[sensor_type] = TemperatureSensor(
                base_temp=simulator_state['sensors'][sensor_type]['base_temp'],
                noise_range=simulator_state['sensors'][sensor_type]['noise_range']
            )
        elif sensor_type == 'humidity':
            sensors[sensor_type].current_humidity = simulator_state['sensors'][sensor_type]['initial_humidity']
        elif sensor_type == 'gps':
            sensors[sensor_type].current_lat = simulator_state['sensors'][sensor_type]['lat']
            sensors[sensor_type].current_lon = simulator_state['sensors'][sensor_type]['lon']
    
    logger.info(f"Paramètres du capteur {sensor_type} mis à jour")
    return jsonify({'status': 'success', 'message': 'Capteur mis à jour'})


@app.route('/api/update_interval', methods=['POST'])
def update_interval():
    """Met à jour l'intervalle de publication."""
    data = request.json
    interval = data.get('interval', 1.0)
    
    if interval < 0.1 or interval > 60:
        return jsonify({'status': 'error', 'message': 'Intervalle invalide (0.1-60s)'})
    
    simulator_state['interval'] = interval
    logger.info(f"Intervalle mis à jour: {interval}s")
    return jsonify({'status': 'success', 'message': f'Intervalle défini à {interval}s'})


@socketio.on('connect')
def handle_connect():
    """Gère la connexion WebSocket."""
    logger.info("Client WebSocket connecté")
    emit('status', simulator_state)


@socketio.on('disconnect')
def handle_disconnect():
    """Gère la déconnexion WebSocket."""
    logger.info("Client WebSocket déconnecté")


if __name__ == '__main__':
    import os
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    
    logger.info("=" * 60)
    logger.info("INTERFACE WEB IoT - Démarrage")
    logger.info("=" * 60)
    logger.info(f"Accédez à l'interface sur: http://{host}:{port}")
    logger.info(f"Contrôles: http://{host}:{port}/control")
    logger.info(f"Dashboard: http://{host}:{port}/dashboard")
    logger.info("=" * 60)
    
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)
