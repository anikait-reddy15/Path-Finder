from flask import Flask, render_template, jsonify, request
import networkx as nx
import math

# Initialize the Flask application
app = Flask(__name__)

# --- Campus Graph Definition ---
G = nx.Graph()

# Latitude and Longitude of Location
locations = {
    "Gate":               { "lat": 17.393684789589315, "lng": 78.31999168654374 },
    "Scrap shed":         { "lat": 17.39339258000706, "lng": 78.31906986268905 },
    "Bus Bay":            { "lat": 17.392613352172084, "lng": 78.31962168112109 },
    "Parking Shed 1":     { "lat": 17.39258319404134, "lng": 78.31973359432149 },
    "Statue":             { "lat": 17.392286416886325, "lng": 78.31959324743322 },
    "Shed 2":             { "lat": 17.4440, "lng": 78.3535 },
    "Shed 3":             { "lat": 17.4442, "lng": 78.3528 },
    "Shed 4":             { "lat": 17.4444, "lng": 78.3521 },
    "Shed 5":             { "lat": 17.4446, "lng": 78.3514 },
    "Fee Counter":        { "lat": 17.4453, "lng": 78.3530 },
    "Food truck":         { "lat": 17.4455, "lng": 78.3515 },
    "AIDS block":         { "lat": 17.4468, "lng": 78.3510 },
    "Civil block":        { "lat": 17.4473, "lng": 78.3525 },
    "CSE block":          { "lat": 17.4473, "lng": 78.3550 },
    "Mechanical block":   { "lat": 17.4473, "lng": 78.3575 },
    "Power control":      { "lat": 17.4473, "lng": 78.3590 },
    "ECE Block":          { "lat": 17.4455, "lng": 78.3585 },
    "Canteen":            { "lat": 17.4493, "lng": 78.3505 },
    "Chem lab":           { "lat": 17.4498, "lng": 78.3520 },
    "Circular Garden":    { "lat": 17.4488, "lng": 78.3545 },
    "Central Workshop":   { "lat": 17.4488, "lng": 78.3570 },
    "House Wiring Lab":   { "lat": 17.4485, "lng": 78.3588 },
    "Library":            { "lat": 17.4495, "lng": 78.3595 },
    "K block":            { "lat": 17.4508, "lng": 78.3525 },
    "Stationery":         { "lat": 17.4505, "lng": 78.3540 },
    "Open Air Audi":      { "lat": 17.4503, "lng": 78.3555 },
    "BEE labs":           { "lat": 17.4501, "lng": 78.3575 },
    "IT block (L block)": { "lat": 17.4508, "lng": 78.3580 },
    "Sports block":       { "lat": 17.4508, "lng": 78.3595 },
    "Robo wars arena":    { "lat": 17.4513, "lng": 78.3545 },
    "Throwball court":    { "lat": 17.4518, "lng": 78.3560 },
    "EDE Block (N block)":{ "lat": 17.4521, "lng": 78.3580 },
    "Biotech block":      { "lat": 17.4521, "lng": 78.3530 },
    "Basketball court":   { "lat": 17.4518, "lng": 78.3598 },
    "Football ground":    { "lat": 17.4522, "lng": 78.3515 },
    "Volleyball court":   { "lat": 17.4523, "lng": 78.3545 },
    "Cricket ground":     { "lat": 17.4525, "lng": 78.3590 },
}

# Add nodes to the graph from the locations dictionary
G.add_nodes_from(locations.keys())

# Define edges (paths) with weights (distances). This remains unchanged.
edges = [
    ("Gate", "Parking Shed 1", 140), ("Gate", "Bus Bay", 150),
    ("Gate", "Scrap shed", 140), ("Scrap shed", "Bus Bay", 140),
    ("Bus Bay", "ECE Block", 100), ("Bus Bay", "Statue", 20),
    ("Parking Shed 1", "Statue", 10), ("Parking Shed 1", "Shed 2", 30),
    ("Shed 2", "Shed 3", 30), ("Shed 3", "Shed 4", 30),
    ("Shed 4", "Shed 5", 30), ("Shed 5", "Food truck", 20),
    ("Shed 4", "Food truck", 20), ("Food truck", "Fee Counter", 60),
    ("Food truck", "AIDS block", 40), ("AIDS block", "Civil block", 40),
    ("AIDS block", "Canteen", 50), ("Civil block", "CSE block", 80),
    ("CSE block", "Mechanical block", 80), ("CSE block", "Statue", 20),
    ("CSE block", "Circular Garden", 10), ("Mechanical block", "Power control", 40),
    ("Mechanical block", "Central Workshop", 30), ("Power control", "ECE Block", 80),
    ("Power control", "House Wiring Lab", 30), ("ECE Block", "Statue", 110),
    ("Statue", "Fee Counter", 60), ("Canteen", "Chem lab", 50),
    ("Canteen", "K block", 70), ("Canteen", "Biotech block", 100),
    ("Canteen", "Football ground", 130), ("Chem lab", "Circular Garden", 90),
    ("Circular Garden", "Open Air Audi", 40),
    ("Circular Garden", "Central Workshop", 120), ("Central Workshop", "House Wiring Lab", 30),
    ("Central Workshop", "BEE labs", 50), ("House Wiring Lab", "Library", 40),
    ("Library", "Sports block", 40), ("Library", "BEE labs", 60),
    ("BEE labs", "Open Air Audi", 60), ("BEE labs", "IT block (L block)", 40),
    ("Open Air Audi", "Stationery", 80), ("Open Air Audi", "Robo wars arena", 40),
    ("IT block (L block)", "EDE Block (N block)", 40), ("IT block (L block)", "Throwball court", 40),
    ("Sports block", "Basketball court", 10), ("Sports block", "EDE Block (N block)", 110),
    ("Basketball court", "EDE Block (N block)", 10), ("EDE Block (N block)", "Throwball court", 40),
    ("EDE Block (N block)", "Biotech block", 60), ("EDE Block (N block)", "Cricket ground", 100),
    ("Throwball court", "Robo wars arena", 40), ("Throwball court", "Volleyball court", 10),
    ("Throwball court", "Biotech block", 80), ("Volleyball court", "Football ground", 10),
    ("Volleyball court", "Cricket ground", 60), ("Robo wars arena", "Stationery", 40),
    ("Stationery", "K block", 60), ("K block", "Biotech block", 100),
]
G.add_weighted_edges_from(edges)

# --- Heuristic function for A* ---
# This uses the manually entered lat/lng values for its calculation.
def heuristic(u, v):
    lat1, lng1 = locations[u]['lat'], locations[u]['lng']
    lat2, lng2 = locations[v]['lat'], locations[v]['lng']
    return math.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)

# --- Routes (No changes) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

# --- API Endpoints (No changes in logic) ---
@app.route('/api/locations')
def get_locations():
    sorted_locations = dict(sorted(locations.items()))
    return jsonify(sorted_locations)

@app.route('/api/find_path')
def find_path():
    start = request.args.get('start')
    end = request.args.get('end')

    if start not in G.nodes or end not in G.nodes:
        return jsonify({"error": "Invalid start or end location."}), 400

    try:
        path = nx.astar_path(G, source=start, target=end, heuristic=heuristic, weight='weight')
        distance = nx.astar_path_length(G, source=start, target=end, heuristic=heuristic, weight='weight')
        return jsonify({"path": path, "distance": round(distance)})
    except nx.NetworkXNoPath:
        return jsonify({"error": f"No path exists between {start} and {end}."}), 404

# Run the server
if __name__ == '__main__':
    app.run(debug=True)