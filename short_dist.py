import networkx as nx
from geopy.distance import geodesic

# Function to geocode addresses into (latitude, longitude)
# For simplicity, we assume you have pre-processed coordinates

def get_coordinates(address):
    # Dummy function to return latitude and longitude for an address
    # You would use Geopy or Google Maps API for real-world geocoding
    address_dict = {
        "source1": (40.748817, -73.985428),  # Example coordinates for source
        "source2": (34.052235, -118.243683),  # Example coordinates for another source
        "dest1": (37.774929, -122.419418),   # Example coordinates for destination
        "dest2": (51.507351, -0.127758)      # Example coordinates for another destination
    }
    return address_dict.get(address, None)

# Function to calculate distance between two coordinates using Geopy
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

# Function to build the graph of sources and destinations
def build_graph(sources, destinations):
    G = nx.Graph()
    
    # Add nodes for sources
    for source in sources:
        G.add_node(source, pos=get_coordinates(source), label='source')
        
    # Add nodes for destinations
    for dest in destinations:
        G.add_node(dest, pos=get_coordinates(dest), label='destination')
    
    # Add edges between every source and destination with the distance as weight
    for source in sources:
        for dest in destinations:
            source_coord = get_coordinates(source)
            dest_coord = get_coordinates(dest)
            if source_coord and dest_coord:
                distance = calculate_distance(source_coord, dest_coord)
                G.add_edge(source, dest, weight=distance)
    
    return G

# Function to find the shortest path between a source and a destination using Dijkstra's Algorithm
def find_shortest_path(G, source, dest):
    try:
        # Use Dijkstra's algorithm to find the shortest path by weight (distance)
        shortest_path = nx.dijkstra_path(G, source, dest, weight='weight')
        shortest_distance = nx.dijkstra_path_length(G, source, dest, weight='weight')
        return shortest_path, shortest_distance
    except nx.NetworkXNoPath:
        return None, float('inf')  # Return infinity if no path exists

# Function to find the nearest source for each destination
def find_nearest_source_for_dest(G, sources, dest):
    nearest_source = None
    shortest_distance = float('inf')
    
    for source in sources:
        path, distance = find_shortest_path(G, source, dest)
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_source = source
            
    return nearest_source, shortest_distance

# Function to predict the best source-destination pairs
def predict_best_matches(G, sources, destinations):
    best_matches = {}
    
    for dest in destinations:
        nearest_source, distance = find_nearest_source_for_dest(G, sources, dest)
        best_matches[dest] = (nearest_source, distance)
    
    return best_matches

# Main function to run the model
def run_model():
    sources = ["source1", "source2"]  # List of source nodes (those with resources)
    destinations = ["dest1", "dest2"]  # List of destination nodes (those in need)
    
    # Build the graph
    G = build_graph(sources, destinations)
    
    # Predict the best matches
    best_matches = predict_best_matches(G, sources, destinations)
    
    for dest, (source, distance) in best_matches.items():
        print(f"Destination {dest} is best served by Source {source} with a distance of {distance:.2f} km")

# Execute the model
run_model()
