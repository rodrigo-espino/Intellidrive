import networkx as nx
import joblib
import osmnx as ox
def get_nearest_node(lat, lon, knn_model, nodes):
    """
    Get nearest node to given location

    param lat: latitude of given location
    type lat: float
    param lon: longitude of given location
    type lon: float
    param knn_model: KNN model
    type knn_model: KNN model
    param nodes: List of nodes provided by `osmnx` library

    return: nearest node to given location
    type nodes: list
    """
    dist, idx = knn_model.kneighbors([(lat, lon)])
    nearest_node = nodes.iloc[idx[0][0]].name
    return nearest_node

def find_route(start_point, end_point, knn_model, G, nodes):
    """
    Find route between given location and given location
    param start_point: starting location
    type start_point: tuple
    param end_point: ending location
    type end_point: tuple
    param knn_model: KNN model
    type knn_model: KNN model
    param G: networkx graph
    type G: networkx graph
    param nodes: List of nodes provided by `osmnx` library

    return: route between given location and given location
    type nodes: list
    """
    start_node = get_nearest_node(start_point[0], start_point[1], knn_model, nodes)
    end_node = get_nearest_node(end_point[0], end_point[1], knn_model, nodes)
    route = nx.shortest_path(G, start_node, end_node, weight='length')
    return route

def extract_route_coordinates(G, route):
    """
    Extract coordinates of route between given location and given location
    param G: networkx graph
    type: networkx graph
    param route: route between given location and given location

    return: coordinates of route between given location and given location
    type route: list
    """
    route_coords = []
    for node in route:
        point = (G.nodes[node]['y'], G.nodes[node]['x'])
        route_coords.append(point)
    return route_coords
