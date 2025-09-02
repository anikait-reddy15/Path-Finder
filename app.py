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
    "Shed 1":             { "lat": 17.39258319404134, "lng": 78.31973359432149 },
    "Statue":             { "lat": 17.392286416886325, "lng": 78.31959324743322 },
    "Shed 2":             { "lat": 17.392586810798218, "lng": 78.32016798725313 },
    "Shed 3":             { "lat": 17.392519770078785, "lng": 78.32043835382032 },
    "Shed 4":             { "lat": 17.392469997407552, "lng": 78.32071723586994 },
    "Shed 5":             { "lat": 17.39241616164589, "lng": 78.32096524929575 },
    "Fee Counter":        { "lat": 17.39211097137123, "lng": 78.32011989741815 },
    "Food truck":         { "lat": 17.39191820922901, "lng": 78.32055964995043 },
    "AIDS block":         { "lat": 17.391578020123948, "lng": 78.32048542148472 },
    "Civil labs":         { "lat": 17.391492200302846, "lng": 78.32044285982616 },
    "Civil block":        { "lat": 17.391700124386396, "lng": 78.32007295864172 },
    "CSE block":          { "lat": 17.39183659375976, "lng": 78.31947383378218 },
    "Mechanical block":   { "lat": 17.39196300740788, "lng": 78.31887771956472 },
    "Power control":      { "lat": 17.392234509147368, "lng": 78.31851643822472 },
    "R and E block":      { "lat": 17.392480153235585, "lng": 78.318414075185 },
    "ECE Block (N block)":{ "lat": 17.391048189483858, "lng": 78.31891851261692 },
    "Canteen":            { "lat": 17.391284860202767, "lng": 78.32059175560758 },
    "Chem lab":           { "lat": 17.39141894252225, "lng": 78.32003399150835 },
    "Circular Garden":    { "lat": 17.391687106866346, "lng": 78.31943790773816 },
    "Central Workshop":   { "lat": 17.391924797668675, "lng": 78.31844585402352 },
    "House Wiring Lab":   { "lat": 17.391924797668675, "lng": 78.31844585402352 },
    "Library":            { "lat": 17.391590920392414,  "lng": 78.31835596318487 },
    "K block":            { "lat": 17.39108214855515,  "lng": 78.3201931454366 },
    "Stationery":         { "lat": 17.391212872293288, "lng": 78.31965423413081 },
    "Open Air Audi":      { "lat": 17.39145708122418, "lng": 78.31923876061013 },
    "BEE labs":           { "lat": 17.391698408426294, "lng": 78.31878524960091 },
    "IT block (L block)": { "lat": 17.3911510045195, "lng": 78.31909624282652 },
    "Sports block":       { "lat": 17.39144051580332, "lng": 78.31820394387495 },
    "Robo wars arena":    { "lat": 17.39113087361985, "lng": 78.31930756426303 },
    "Throwball court":    { "lat": 17.390849372170376, "lng": 78.31902113009522 },
    "Biotech block":      { "lat": 17.390761462109463, "lng": 78.3194527512126 },
    "Basketball court":   { "lat": 17.39112421342946, "lng": 78.3180658218862 },
    "Football ground":    { "lat": 17.390116779438245, "lng": 78.31958977713342 },
    "Volleyball court":   { "lat": 17.390421188932503, "lng": 78.31925053361154 },
    "Cricket ground":     { "lat": 17.39077150081885, "lng": 78.3185315398786 },
}

# Add nodes to the graph from the locations dictionary
G.add_nodes_from(locations.keys())

# Define edges (paths) with weights (distances).
edges = [
    ("Gate", "Shed 1", 140),
    ("Gate", "Bus Bay", 140),
    ("Gate", "Scrap shed", 140),
    ("Gate", "Statue", 160),
    ("Scrap shed", "R and E block", 100),
    ("Bus Bay", "Shed 1", 10),
    ("Bus Bay", "R and E block", 170),
    ("Bus Bay", "Statue", 20),
    ("Shed 1", "Statue", 20),
    ("Shed 1", "Shed 2", 30),
    ("Shed 2", "Shed 3", 30),
    ("Shed 3", "Shed 4", 30),
    ("Shed 4", "Shed 5", 30),
    ("Shed 5", "Food truck", 20),
    ("Shed 4", "Food truck", 20),
    ("Food truck", "Fee Counter", 60),
    ("Food truck", "AIDS block", 40),
    ("AIDS block", "Civil block", 40),
    ("AIDS block", "Civil labs", 10),
    ("R and E block", "Power control", 40),
    ("AIDS block", "Canteen", 50),
    ("Civil block", "CSE block", 80),
    ("CSE block", "Mechanical block", 80),
    ("CSE block", "Statue", 20),
    ("CSE block", "Circular Garden", 10),
    ("Mechanical block", "Power control", 40),
    ("Power control", "Central Workshop", 30),
    ("Mechanical block", "R and E block", 80),
    ("Power control", "House Wiring Lab", 30),
    ("R and E block", "Statue", 110),
    ("Statue", "Fee Counter", 60),
    ("Canteen", "Chem lab", 50),
    ("Canteen", "K block", 70),
    ("Canteen", "Biotech block", 100),
    ("Canteen", "Football ground", 130),
    ("Chem lab", "Circular Garden", 60),
    ("Chem lab", "Open Air Audi", 80),
    ("Circular Garden", "Open Air Audi", 40),
    ("Circular Garden", "Central Workshop", 120),
    ("Central Workshop", "Library", 40),
    ("Central Workshop", "BEE labs", 50),
    ("House Wiring Lab", "Library", 40),
    ("House Wiring Lab", "Mechanical block", 60),
    ("Library", "Sports block", 30),
    ("Library", "BEE labs", 60),
    ("BEE labs", "Open Air Audi", 60),
    ("Open Air Audi", "IT block (L block)", 40),
    ("Open Air Audi", "Stationery", 80),
    ("Open Air Audi", "Robo wars arena", 40),
    ("IT block (L block)", "ECE Block (N block)", 40),
    ("IT block (L block)", "Throwball court", 40),
    ("Sports block", "Basketball court", 10),
    ("Sports block", "ECE Block (N block)", 110),
    ("Sports block", "IT block (L block)", 120),
    ("Basketball court", "ECE Block (N block)", 10),
    ("ECE Block (N block)", "Throwball court", 40),
    ("Throwball court", "Cricket ground", 60),
    ("ECE Block (N block)", "Cricket ground", 100),
    ("Throwball court", "Robo wars arena", 40),
    ("Throwball court", "Volleyball court", 10),
    ("Throwball court", "Biotech block", 80),
    ("Volleyball court", "Football ground", 10),
    ("Volleyball court", "Cricket ground", 60),
    ("Robo wars arena", "Stationery", 40),
    ("Stationery", "K block", 60),
    ("K block", "Biotech block", 30),
    ("K block", "Robo wars arena", 100),
    ("Biotech block", "Football ground", 40),
    ("Civil block", "Fee Counter", 20),
]

G.add_weighted_edges_from(edges)

# --- Heuristic function for A* ---
def heuristic(u, v):
    lat1, lng1 = locations[u]['lat'], locations[u]['lng']
    lat2, lng2 = locations[v]['lat'], locations[v]['lng']
    # A simple Euclidean distance heuristic
    return math.sqrt((lat1 - lat2)**2 + (lng1 - lng2)**2)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def app_page():
    return render_template('app.html')

# --- API Endpoints ---
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
        # This will now correctly trigger if a path truly doesn't exist
        return jsonify({"error": f"No path exists between {start} and {end}."}), 404
    except Exception as e:
        print(f"An unexpected error occurred in find_path: {e}") 
        return jsonify({"error": "A server error occurred during path calculation."}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)

