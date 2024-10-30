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
        # """Crear mapa de contaminación de México"""
        # # Crear mapa base
        # m = folium.Map(
        #     location=self.center,
        #     zoom_start=5,
        #     tiles='cartodbpositron'
        # )
        
        # # Obtener datos de contaminación
        # pollution_data = self.pollution_service.get_all_states_pollution()
        
        # # Crear escala de colores
        # colormap = LinearColormap(
        #     colors=['green', 'yellow', 'orange', 'red', 'purple'],
        #     vmin=0,
        #     vmax=300,
        #     caption='Índice de Calidad del Aire (AQI)'
        # )
        # colormap.add_to(m)
        
        # # Añadir marcadores para cada estado
        # print(f"Number of states: {len(pollution_data)}")
        # for state, data in pollution_data.items():
        #     if data and 'aqi' in data:
        #         print(f"Processing state: {state}")
        #         color = self._get_color_by_aqi(data['aqi'])
        #         print(f"Color for AQI {data['aqi']}: {color}")
        #         # Crear popup con información detallada
        #         popup_html = self._create_popup_html(data)
                
        #         try:
        #             lat, lon = float(data['lat']), float(data['lon'])
        #         except ValueError:
        #             print(f"Invalid coordinates for {state}: lat={data['lat']}, lon={data['lon']}")
        #             continue
        #         # Añadir círculo al mapa
        #         circle = folium.Circle(
        #             location=[lat, lon],
        #             radius=25000,  # 25km
        #             popup=popup_html,
        #             color=color,
        #             fill=True,
        #             fillColor=color,
        #             fillOpacity=0.7,
        #         )

                
        #         # Añadir etiqueta del estado
        #         folium.Tooltip(
        #             f"{state}: AQI {data['aqi']}"
        #         ).add_to(circle)

        #         circle.add_to(m)
        
        """Crear mapa de contaminación de México"""
        # Crear mapa base
        m = folium.Map(
            location=self.center,
            zoom_start=5,
            tiles='cartodbpositron'
        )
        
        # Obtener datos de contaminación
        pollution_data = self.pollution_service.get_all_station_pollution_in_mexico()
        
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
        for data in pollution_data:
            if data and 'aqi' in data:
                color = self._get_color_by_aqi(data['aqi'])
                print(f"Color for AQI {data['aqi']}: {color}")
                # Crear popup con información detallada
                popup_html = self._create_popup_html(data)
                
                try:
                    lat, lon = float(data['lat']), float(data['lon'])
                except ValueError:
                    continue
                # Añadir círculo al mapa
                circle = folium.Circle(
                    location=[lat, lon],
                    radius=25000,  # 25km
                    popup=popup_html,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.5,
                )

                
                # Añadir etiqueta del estado
                folium.Tooltip(
                    f"{data['station']['name']}: AQI {data['aqi']}"
                ).add_to(circle)

                circle.add_to(m)
        
        return m

    def local_pollution_map(self):
        """Crear mapa de contaminación de México"""

        
        # Obtener datos de contaminación
        pollution_data = self.pollution_service.get_local_pollution()

        name = pollution_data['city']['name']
        lat = pollution_data['city']['geo'][0]
        lon = pollution_data['city']['geo'][1]
        aqi = pollution_data['aqi']

        # Crear mapa base
        m = folium.Map(
            location=[lat, lon],
            zoom_start=9,
            tiles='cartodbpositron'
        )
        
        # Crear escala de colores
        colormap = LinearColormap(
            colors=['green', 'yellow', 'orange', 'red', 'purple'],
            vmin=0,
            vmax=300,
            caption='Índice de Calidad del Aire (AQI)'
        )
        colormap.add_to(m)
        

        if 'aqi' in pollution_data:
            print(f"Processing state: {name}")
            color = self._get_color_by_aqi(aqi)
            # Crear popup con información detallada
            popup_html = self._create_local_popup_html(pollution_data)
            
            try:
                lat, lon = float(lat), float(lon)
            except ValueError:
                print(f"Invalid coordinates for {name}: lat={lat}, lon={lon}")
   
            # Añadir círculo al mapa
            circle = folium.Circle(
                location=[lat, lon],
                radius=25000,  # 25km
                popup=popup_html,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.5,
            )

                
            # Añadir etiqueta del estado
            folium.Tooltip(
                f"{name}: AQI {aqi}"
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
                <h4>{data['station']['name']}</h4>
                <p><b>AQI:</b> {data['aqi']}</p>
                <p><b>Latitud:</b> {data['lat']}</p>
                <p><b>Longitud:</b> {data['lon']}</p>
            </div>
        """)
    
    def _create_local_popup_html(self, data):
        """Crear contenido HTML para el popup"""
        return folium.Popup(f"""
            <div style="width:200px">
                <h4>{data['city']['name']}</h4>
                <p><b>AQI:</b> {data['aqi']}</p>
                <p><b>Latitud:</b> {data['city']['geo'][0]}</p>
                <p><b>Longitud:</b> {data['city']['geo'][0]}</p>
                <p><b>Dominentpol:</b> {data['dominentpol']}</p>
                {''.join([f"<p><b>{pollutant}:</b> {value['v']}</p>" for pollutant, value in data['iaqi'].items()])}
            </div>
        """)
