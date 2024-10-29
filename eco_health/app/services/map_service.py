# app/services/map_service.py
import folium
from folium import plugins
from branca.colormap import LinearColormap
from .pollution_service import PollutionService

class MapService:
    def __init__(self):
        self.center = [23.6345, -102.5528]  # Centro de México
        self.pollution_service = PollutionService()
        
    def create_pollution_map(self):
        """Crear mapa de contaminación de México"""
        # Crear mapa base
        m = folium.Map(
            location=self.center,
            zoom_start=5,
            tiles='cartodbpositron'
        )
        
        # Obtener datos de contaminación
        pollution_data = self.pollution_service.get_all_states_pollution()
        
        # Crear escala de colores
        colormap = LinearColormap(
            colors=['green', 'yellow', 'orange', 'red', 'purple'],
            vmin=0,
            vmax=300,
            caption='Índice de Calidad del Aire (AQI)'
        )
        colormap.add_to(m)
        
        # Añadir marcadores para cada estado
        print(f"Number of states: {len(pollution_data)}")
        for state, data in pollution_data.items():
            if data and 'aqi' in data:
                print(f"Processing state: {state}")
                color = self._get_color_by_aqi(data['aqi'])
                print(f"Color for AQI {data['aqi']}: {color}")
                # Crear popup con información detallada
                popup_html = self._create_popup_html(data)
                
                try:
                    lat, lon = float(data['lat']), float(data['lon'])
                except ValueError:
                    print(f"Invalid coordinates for {state}: lat={data['lat']}, lon={data['lon']}")
                    continue
                # Añadir círculo al mapa
                circle = folium.Circle(
                    location=[lat, lon],
                    radius=25000,  # 25km
                    popup=popup_html,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                )

                
                # Añadir etiqueta del estado
                folium.Tooltip(
                    f"{state}: AQI {data['aqi']}"
                ).add_to(circle)

                circle.add_to(m)
        
        return m
    
    def _get_color_by_aqi(self, aqi):
        """Determinar color basado en AQI"""
        try:
            aqi = float(aqi)
        except ValueError:
            return 'gray'

        if aqi <= 50:
            return 'green'
        elif aqi <= 100:
            return 'yellow'
        elif aqi <= 150:
            return 'orange'
        elif aqi <= 200:
            return 'red'
        return 'purple'
    
    def _create_popup_html(self, data):
        """Crear contenido HTML para el popup"""
        return folium.Popup(f"""
            <div style="width:200px">
                <h4>{data['name']}</h4>
                <p><b>AQI:</b> {data['aqi']}</p>
                <p><b>Principal contaminante:</b> {data['dominentpol']}</p>
                <p><b>Última actualización:</b> {data['time'].get('s', 'N/A')}</p>
                <hr>
                <p><b>Detalles:</b></p>
                <ul>
                    {''.join([
                        f"<li>{k}: {v.get('v', 'N/A')}</li>"
                        for k, v in data['iaqi'].items()
                    ])}
                </ul>
            </div>
        """)