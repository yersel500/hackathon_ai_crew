# app/routes/map_routes.py
from flask import Blueprint, render_template, jsonify, request
from ..services.map_service import MapService
from ..services.pollution_service import PollutionService
from ..routes.user_routes import token_required 

map_routes = Blueprint('map_routes', __name__)
map_service = MapService()

@map_routes.route('/')
@token_required
def index():
    return "EcoHealth API is running!"

@map_routes.route('/map')
@token_required
def show_map(current_user):
    try:
        print("\n--- Entering show_map function ---")
        print(f"Request method: {request.method}")
        print(f"Request path: {request.path}")
        print(f"Request headers:")
        for header, value in request.headers:
            print(f"  {header}: {value}")
        print("Request cookies:")
        for key, value in request.cookies.items():
            print(f"  {key}: {value}")
        
        # Print raw cookie string
        raw_cookies = request.headers.get('Cookie')
        print(f"Raw Cookie string: {raw_cookies}")
        
        # Manually parse cookies
        cookies = {}
        if raw_cookies:
            for cookie in raw_cookies.split(';'):
                parts = cookie.strip().split('=')
                if len(parts) == 2:
                    cookies[parts[0]] = parts[1]
        
        print("Manually parsed cookies:")
        for key, value in cookies.items():
            print(f"  {key}: {value}")
        
        token = cookies.get('token') or request.cookies.get('token')
        print(f"\nToken from cookie: {token}")
        
        print(f"Showing map for user: {current_user['email']}")
        map1 = map_service.create_pollution_map()
        if not map1:
            print("Error creating map")
            return "Error creating the map", 500
        print("Map created successfully")

        # Create the second map
        map2 = map_service.local_pollution_map()
        if not map2:
            print("Error creating second map")
            return "Error creating the second map", 500
        print("Second map created successfully")

        print("--- Exiting show_map function ---\n")
        return render_template('map.html', map1_html=map1._repr_html_(), map2_html=map2._repr_html_())
    except Exception as e:
        print(f"Error in show_map: {str(e)}")
        return str(e), 500

@map_routes.route('/api/pollution')
@token_required
def get_pollution_data():
    pollution_service = PollutionService()
    data = pollution_service.get_all_states_pollution()
    return jsonify(data)