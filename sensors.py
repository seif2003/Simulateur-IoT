"""
Module contenant les classes de capteurs IoT simulés.
Chaque capteur génère des données réalistes avec du bruit aléatoire.
"""

import random
import math
from datetime import datetime, timezone
from typing import Dict, Any


class TemperatureSensor:
    """
    Capteur de température simulé avec bruit aléatoire.
    """
    
    def __init__(self, base_temp: float = 22.0, noise_range: float = 2.0):
        """
        Initialise le capteur de température.
        
        Args:
            base_temp: Température centrale en °C (par défaut 22°C)
            noise_range: Amplitude du bruit aléatoire (par défaut ±2°C)
        """
        self.base_temp = base_temp
        self.noise_range = noise_range
        self.sensor_name = "temperature"
    
    def read(self) -> Dict[str, Any]:
        """
        Génère une lecture de température avec bruit aléatoire.
        
        Returns:
            Dictionnaire contenant timestamp, sensor, value et unit
        """
        # Bruit aléatoire gaussien pour simuler un capteur réel
        noise = random.gauss(0, self.noise_range / 3)
        temperature = self.base_temp + noise
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor": self.sensor_name,
            "value": round(temperature, 2),
            "unit": "°C"
        }


class HumiditySensor:
    """
    Capteur d'humidité simulé avec variation lente dans le temps.
    """
    
    def __init__(self, initial_humidity: float = 50.0):
        """
        Initialise le capteur d'humidité.
        
        Args:
            initial_humidity: Valeur initiale d'humidité en % (par défaut 50%)
        """
        self.current_humidity = initial_humidity
        self.sensor_name = "humidity"
        self.min_humidity = 20.0
        self.max_humidity = 80.0
    
    def read(self) -> Dict[str, Any]:
        """
        Génère une lecture d'humidité avec variation lente.
        
        Returns:
            Dictionnaire contenant timestamp, sensor, value et unit
        """
        # Variation lente : changement aléatoire de ±2% par lecture
        variation = random.uniform(-2.0, 2.0)
        self.current_humidity += variation
        
        # Contraindre entre min et max
        self.current_humidity = max(self.min_humidity, 
                                   min(self.max_humidity, self.current_humidity))
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor": self.sensor_name,
            "value": round(self.current_humidity, 2),
            "unit": "%"
        }


class GPSSensor:
    """
    Capteur GPS simulé avec déplacement aléatoire.
    """
    
    def __init__(self, initial_lat: float = 48.8566, initial_lon: float = 2.3522):
        """
        Initialise le capteur GPS.
        
        Args:
            initial_lat: Latitude initiale (par défaut Paris: 48.8566)
            initial_lon: Longitude initiale (par défaut Paris: 2.3522)
        """
        self.current_lat = initial_lat
        self.current_lon = initial_lon
        self.sensor_name = "gps"
        
        # Conversion approximative : 1 degré ≈ 111 km
        # Pour quelques mètres de déplacement : 10m ≈ 0.00009 degrés
        self.max_movement = 0.0001  # ≈ 11 mètres
    
    def read(self) -> Dict[str, Any]:
        """
        Génère une lecture GPS avec déplacement aléatoire.
        
        Returns:
            Dictionnaire contenant timestamp, sensor, lat, lon et unit
        """
        # Déplacement aléatoire dans une direction aléatoire
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, self.max_movement)
        
        # Mise à jour de la position
        self.current_lat += distance * math.cos(angle)
        self.current_lon += distance * math.sin(angle)
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor": self.sensor_name,
            "lat": round(self.current_lat, 6),
            "lon": round(self.current_lon, 6),
            "unit": "degrees"
        }
