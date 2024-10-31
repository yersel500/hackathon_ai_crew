# app/services/pollution_service.py
import requests
from typing import Dict, Any

class PollutionService:
    def __init__(self):
        self.api_key = "aa2f064b4d63a6ddaa773654545e19e1884daa1e"
        self.base_url = "https://api.waqi.info/feed"
        
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
            print("Data:", data)

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
        print("Pollution data for all states:", pollution_data)
        return pollution_data
    
    def get_all_station_pollution_in_mexico(self) -> Dict[str, Any]:
        """Obtiene datos de contaminación para un estado específico"""
        try:           
            url = "https://api.waqi.info/v2/map/bounds?latlng=14.538828,-118.364896,32.718655,-86.710288&networks=all&token=aa2f064b4d63a6ddaa773654545e19e1884daa1e"
            response = requests.get(url)
            data = response.json()
            print("Data:", data)

            if data.get('status') == 'ok':
                return data['data']
            return None
        except Exception as e:
            print(f"Error getting pollution data: {e}")
            return None
        

    def get_local_pollution(self) -> Dict[str, Any]:
        """Obtiene datos de contaminación para un estado específico"""
        try:           
            url = "https://api.waqi.info/feed/here/?token=aa2f064b4d63a6ddaa773654545e19e1884daa1e"
            response = requests.get(url)
            data = response.json()
            print("Data:", data)

            if data.get('status') == 'ok':
                return data['data']
            return None
        except Exception as e:
            print(f"Error getting local pollution data {e}")
            return None