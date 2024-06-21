from flask import Flask, request, jsonify, Blueprint
from .functions import find_route, extract_route_coordinates
from flask_swagger_ui import get_swaggerui_blueprint
import joblib
import osmnx as ox
import requests
import os
from dotenv import load_dotenv

load_dotenv()
SERVER = os.getenv('SERVER')
TOKEN = os.getenv('ACCESS_TOKEN')
bp = Blueprint('main', __name__)

SWAGGER_URL = '/api/docs'
DOCS_URL = '/static/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    DOCS_URL,
    config={
        'app_name': 'IntelliDrive Docs'
    }
)

bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

knn_model = joblib.load('app/knn_model.pkl')
place_name = "Victoria de Durango, Mexico"
G = ox.graph_from_place(place_name, network_type='drive')
nodes = ox.graph_to_gdfs(G, nodes=True, edges=False)

@bp.route("/api/route", methods=['POST'])
def hello_world():
    data = request.get_json()
    print(data[0]['x_initial'])

    x_initial = data[0]['x_initial']
    y_initial = data[0]['y_initial']

    x_final = data[0]['x_final']
    y_final = data[0]['y_final']

    initial_coords = (x_initial, y_initial)
    final_coords = (x_final, y_final)

    route = find_route(initial_coords, final_coords, knn_model, G, nodes)
    coords_route = extract_route_coordinates(G,route)

    headers = {"Content-Type": "application/json; charset=utf-8",
               "Authorization": TOKEN}
    json_body = {
        "to": str(final_coords),
        "from": str(initial_coords),
        "route": str(coords_route),
    }
    try:
        res = requests.post(f'{SERVER}/api/collections/rutas/records', json=json_body, headers=headers)
        return res.json()

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
