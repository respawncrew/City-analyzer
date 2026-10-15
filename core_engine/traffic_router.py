
import networkx as nx
import matplotlib.pyplot as plt

class TrafficRouter:
    def __init__(self):
        # Ek directed graph bana rahe hain city roads ke liye
        self.road_network = nx.DiGraph()
        print("--> Traffic Router & Graph Network engine initialize ho gaya hai!")

    def setup_city_intersections(self):
        # Kuch sample intersections (Chowk/Locations) aur unke beech ki sadkein (edges) jod rahe hain
        intersections = [
            ("Civil Lines", "Railway Station", {"weight": 4.5, "traffic_load": "Low"}),
            ("Railway Station", "City Hospital", {"weight": 3.0, "traffic_load": "Medium"}),
            ("Civil Lines", "Main Market", {"weight": 2.0, "traffic_load": "High"}),
            ("Main Market", "City Hospital", {"weight": 5.2, "traffic_load": "Low"}),
            ("City Hospital", "University Gate", {"weight": 3.8, "traffic_load": "Medium"})
        ]
        
        self.road_network.add_edges_from(intersections)
        print("--> Road network graph mein intersections aur routes map ho gaye hain.")

    def find_shortest_path(self, start_node, end_node):
        try:
            # Dijkstra algorithm se sabse fast aur chota rasta nikalna
            path = nx.shortest_path(self.road_network, source=start_node, target=end_node, weight='weight')
            print(f"--> Fastest Route from {start_node} to {end_node}: {' -> '.join(path)}")
            return path
        except Exception as e:
            print(f"--> Rasta dhoondhne mein dikkat aayi: {e}")
            return []

# Test karne ke liye
if __name__ == "__main__":
    router = TrafficRouter()
    router.setup_city_intersections()
    router.find_shortest_path("Civil Lines", "City Hospital")