"""
Module gérant la connexion et la publication MQTT.
Encapsule la logique de communication avec le broker MQTT.
"""

import json
import time
import logging
from typing import Dict, Any, Optional
import paho.mqtt.client as mqtt


# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MQTTClient:
    """
    Client MQTT pour publier les données des capteurs.
    Gère la connexion, reconnexion automatique et publication JSON.
    """
    
    def __init__(
        self,
        broker_host: str = "localhost",
        broker_port: int = 1883,
        client_id: str = "iot_simulator",
        keepalive: int = 60
    ):
        """
        Initialise le client MQTT.
        
        Args:
            broker_host: Adresse du broker MQTT
            broker_port: Port du broker MQTT
            client_id: Identifiant unique du client
            keepalive: Intervalle de keepalive en secondes
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id
        self.keepalive = keepalive
        self.connected = False
        
        # Création du client MQTT
        self.client = mqtt.Client(client_id=self.client_id)
        
        # Configuration des callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
    
    def _on_connect(self, client, userdata, flags, rc):
        """
        Callback appelé lors de la connexion au broker.
        
        Args:
            client: Instance du client MQTT
            userdata: Données utilisateur
            flags: Flags de connexion
            rc: Code de retour de connexion
        """
        if rc == 0:
            self.connected = True
            logger.info(f"✓ Connecté au broker MQTT {self.broker_host}:{self.broker_port}")
        else:
            self.connected = False
            logger.error(f"✗ Échec de connexion au broker. Code: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """
        Callback appelé lors de la déconnexion du broker.
        
        Args:
            client: Instance du client MQTT
            userdata: Données utilisateur
            rc: Code de retour de déconnexion
        """
        self.connected = False
        if rc != 0:
            logger.warning(f"⚠ Déconnexion inattendue du broker. Code: {rc}")
            logger.info("↻ Tentative de reconnexion automatique...")
        else:
            logger.info("✓ Déconnexion propre du broker")
    
    def _on_publish(self, client, userdata, mid):
        """
        Callback appelé après publication d'un message.
        
        Args:
            client: Instance du client MQTT
            userdata: Données utilisateur
            mid: Message ID
        """
        logger.debug(f"Message {mid} publié avec succès")
    
    def connect(self, timeout: int = 10) -> bool:
        """
        Connecte le client au broker MQTT avec timeout.
        
        Args:
            timeout: Timeout de connexion en secondes
            
        Returns:
            True si connecté, False sinon
        """
        try:
            logger.info(f"Connexion au broker MQTT {self.broker_host}:{self.broker_port}...")
            self.client.connect(self.broker_host, self.broker_port, self.keepalive)
            self.client.loop_start()
            
            # Attendre la connexion
            elapsed = 0
            while not self.connected and elapsed < timeout:
                time.sleep(0.5)
                elapsed += 0.5
            
            if not self.connected:
                logger.error(f"Timeout de connexion après {timeout}s")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur de connexion: {e}")
            return False
    
    def disconnect(self):
        """
        Déconnecte proprement le client du broker.
        """
        logger.info("Déconnexion du broker MQTT...")
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
    
    def publish(
        self,
        topic: str,
        data: Dict[str, Any],
        qos: int = 1,
        retain: bool = False
    ) -> bool:
        """
        Publie un message JSON sur un topic MQTT.
        
        Args:
            topic: Topic MQTT de destination
            data: Dictionnaire de données à publier
            qos: Quality of Service (0, 1 ou 2)
            retain: Si True, le message est retained par le broker
            
        Returns:
            True si publié, False sinon
        """
        if not self.connected:
            logger.warning("⚠ Client non connecté, publication impossible")
            return False
        
        try:
            # Sérialisation en JSON
            payload = json.dumps(data, ensure_ascii=False)
            
            # Publication du message
            result = self.client.publish(topic, payload, qos=qos, retain=retain)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"→ [{topic}] {payload}")
                return True
            else:
                logger.error(f"✗ Erreur de publication sur {topic}")
                return False
                
        except Exception as e:
            logger.error(f"✗ Exception lors de la publication: {e}")
            return False
    
    def is_connected(self) -> bool:
        """
        Vérifie si le client est connecté au broker.
        
        Returns:
            True si connecté, False sinon
        """
        return self.connected
