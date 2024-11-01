# app/routes/map_routes.py
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from ..services.map_service import MapService
from ..services.pollution_service import PollutionService

map_routes = Blueprint('map_routes', __name__)
map_service = MapService()

@map_routes.route('/map')
@login_required
def show_map():
        map1 = map_service.create_pollution_map()
        if not map1:
            print("Error creating map")
            return "Error creating the map", 500
        print("Map created successfully")

        # Create the second map and forecast table
        map2, forecast_table, name = map_service.local_pollution_map()
        if not map2:
            print("Error creating second map")
            return "Error creating the second map", 500
        print("Second map created successfully")
        
        print("--- Exiting show_map function ---\n")
        return render_template('map.html', map1_html=map1._repr_html_(), map2_html=map2._repr_html_(), forecast_table=forecast_table, name=name)

@map_routes.route('/api/pollution')
@login_required
def get_pollution_data():
    pollution_service = PollutionService()
    data = pollution_service.get_all_states_pollution()
    return jsonify(data)