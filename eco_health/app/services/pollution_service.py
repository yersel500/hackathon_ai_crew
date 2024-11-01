# app/services/pollution_service.py
import requests
from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

class PollutionService:
    def __init__(self):
        self.api_key = os.getenv('AIR_QUALITY_API_KEY')
        self.base_url = os.getenv('AIR_QUALITY_API_URL')
        
        # Diccionario de estados mexicanos con sus coordenadas aproximadas
        self.mexican_states = {
            "Aguascalientes": {"name": "Aguascalientes", "lat": 21.8818, "lon": -102.2916},
            "Baja California": {"name": "Mexicali", "lat": 32.6278, "lon": -115.4545},
            "Chihuahua": {"name": "Chihuahua", "lat": 28.6353, "lon": -106.0889},
            "Ciudad de México": {"name": "Mexico", "lat": 19.4326, "lon": -99.1332},
            "Coahuila": {"name": "Saltillo", "lat": 25.4267, "lon": -101.0029},
            "Colima": {"name": "Colima", "lat": 19.2433, "lon": -103.7247},
            "Durango": {"name": "Durango", "lat": 24.0277, "lon": -104.6532},
            "Estado de México": {"name": "Toluca", "lat": 19.2826, "lon": -99.6557},
            "Guanajuato": {"name": "Guanajuato", "lat": 21.0190, "lon": -101.2574},
            "Hidalgo": {"name": "Pachuca", "lat": 20.1011, "lon": -98.7591},
            "Jalisco": {"name": "Guadalajara", "lat": 20.6597, "lon": -103.3496},
            "Michoacán": {"name": "Morelia", "lat": 19.7060, "lon": -101.1950},
            "Morelos": {"name": "Cuernavaca", "lat": 18.9242, "lon": -99.2216},
            "Nayarit": {"name": "Tepic", "lat": 21.5039, "lon": -104.8946},
            "Nuevo León": {"name": "Monterrey", "lat": 25.6866, "lon": -100.3161},
            "Oaxaca": {"name": "Oaxaca", "lat": 17.0732, "lon": -96.7266},
            "Puebla": {"name": "Puebla", "lat": 19.0413, "lon": -98.2062},
            "Tlaxcala": {"name": "Tlaxcala", "lat": 19.3181, "lon": -98.2375},
            "Veracruz": {"name": "Xalapa", "lat": 19.5438, "lon": -96.9102},
            "Yucatán": {"name": "Merida", "lat": 20.9767, "lon": -89.6217},
            "Zacatecas": {"name": "Zacatecas", "lat": 22.7709, "lon": -102.5832},
        }

    def get_state_pollution(self, state_name: str) -> Dict[str, Any]:
        """Obtiene datos de contaminación para un estado específico"""
        try:
            state = self.mexican_states.get(state_name)
            if not state:
                return None
            
            url = f"{self.base_url}/{state['name']}/?token={self.api_key}"
            response = requests.get(url)
            data = response.json()

            if data.get('status') == 'ok':
                return {
                    'name': state['name'],
                    'aqi': data['data']['aqi'],
                    'lat': data['data']['city']['geo'][0],
                    'lon': data['data']['city']['geo'][1],
                    'dominentpol': data['data'].get('dominentpol', ''),
                    'iaqi': data['data'].get('iaqi', {}),
                    'time': data['data'].get('time', {})
                }
            return None
        except Exception as e:
            print(f"Error getting pollution data for {state_name}: {e}")
            return None

    def get_all_states_pollution(self) -> Dict[str, Any]:
        """Obtiene datos de contaminación para todos los estados"""
        pollution_data = {}
        for state in self.mexican_states:
            data = self.get_state_pollution(state)
            if data:
                pollution_data[state] = data
        return pollution_data
    
    def get_all_station_pollution_in_mexico(self) -> Dict[str, Any]:
        """Obtiene datos de contaminación para un estado específico"""
        try:           
            url = f"{self.base_url}/v2/map/bounds?latlng=14.5329,-125.0,49.384358,-66.93457&networks=all&token={self.api_key}"
            response = requests.get(url)
            data = response.json()

            if data.get('status') == 'ok':
                return data['data']
            return None
        except Exception as e:
            print(f"Error getting pollution data: {e}")
            return None
        

    def get_local_pollution(self) -> Dict[str, Any]:
        """Obtiene datos de contaminación para un estado específico"""
        try:           
            url = f"{self.base_url}/feed/here/?token={self.api_key}"
            response = requests.get(url)
            data = response.json()

            if data.get('status') == 'ok':
                return data['data']
            return None
        except Exception as e:
            print(f"Error getting local pollution data {e}")
            return None