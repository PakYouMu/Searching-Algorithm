import time
import math
import random
import tkinter as tk
from queue import PriorityQueue

class WeightedGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node, neighbor, weight):
        if node not in self.graph:
            self.graph[node] = {}
        if neighbor not in self.graph:
            self.graph[neighbor] = {}

        self.graph[node][neighbor] = weight
        self.graph[neighbor][node] = weight

graph = WeightedGraph()

possible_edges = [
    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'),
    ('D', 'G'), ('D', 'H'), ('E', 'I'), ('E', 'F'), ('F', 'J'), ('G', 'K'), ('H', 'L'),
    ('I', 'M'), ('J', 'N'), ('K', 'O'), ('L', 'M'), ('L', 'N'), ('M', 'O'), ('N', 'O')
]

# Shuffle the list of edges
random.shuffle(possible_edges)

# Assign randomized weights to edges and add them to the graph
for edge in possible_edges:
    weight = random.randint(1, 10)  # Random weight between 1 and 10
    graph.add_edge(edge[0], edge[1], weight)


class AStarApp:
    def __init__(self, master):
        self.master = master
        master.title("A* Pathfinding Visualization")

        self.heading_label = tk.Label(master, text="A* Pathfinding Visualization", bg="White", fg="Black", font=("Times New Roman", 20, "bold", "italic"))
        self.heading_label.pack()

        self.canvas = tk.Canvas(master, width=700, height=700, bg="white")
        self.canvas.pack()

        self.start_node_label = tk.Label(master, text="Start Node:")
        self.start_node_label.pack()

        self.start_node_entry = tk.Entry(master)
        self.start_node_entry.pack()

        self.search_node_label = tk.Label(master, text="Search Node:")
        self.search_node_label.pack()

        self.search_node_entry = tk.Entry(master)
        self.search_node_entry.pack()

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        self.start = tk.Button(master, text="Start", command=self.start_clicked)
        self.start.pack()
        
        self.search_successful = False

        self.vertices = {
                            'A': (100, 50), 'B': (360, 90), 'C': (495, 350), 'D': (100, 160), 'E': (360, 290),
                            'F': (650, 290), 'G': (100, 290), 'H': (220, 220), 'I': (550, 150), 'J': (600, 160),
                            'K': (100, 450), 'L': (360, 520), 'M': (560, 450), 'N': (600, 520), 'O': (220, 360)
                        }
                                
        vertex_names = list(self.vertices.keys())
        random.shuffle(vertex_names)
        randomized_vertices = {key: self.vertices[value] for key, value in zip(vertex_names, vertex_names)}

        self.speed_var = tk.DoubleVar()
        self.speed_scale = tk.Scale(master, from_=0.1, to=2.0, orient=tk.HORIZONTAL, resolution=0.1, label="Simulation Speed", variable=self.speed_var)
        self.speed_scale.set(1.0)
        self.speed_scale.pack()
        self.speed_scale.pack_forget()

        self.reset_var = tk.BooleanVar()
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_app)
        self.reset_button.pack()

        for node, pos in self.vertices.items():
            self.draw_node(node, pos)
            for neighbor, weight in graph.graph[node].items():
                self.draw_edge(node, neighbor, weight)

        self.open_set = PriorityQueue()
        self.closed_set = set()

        self.path_label = tk.Label(master, text="")
        self.path_label.pack()

        self.a_star_running = False

    def draw_node(self, node, pos):
        x, y = pos
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='white')
        self.canvas.create_text(x, y, text=node, font=("Helvetica", 14, 'bold'), fill="black")

    def draw_edge(self, node1, node2, weight):
        x1, y1 = self.vertices[node1]
        x2, y2 = self.vertices[node2]

        line = self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        self.canvas.create_text(mid_x, mid_y, text=str(weight), font=('Times New Roman', 10, 'bold'), fill='red')

    def update_node_color(self, node, color):
        x, y = self.vertices[node]
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color)
        self.canvas.create_text(x, y, text=node, font=('Times New Roman', 14, 'bold'))

    def reset_app(self):
        self.master.destroy()

        # Create a new instance of the app to restart it
        new_root = tk.Tk()
        app = AStarApp(new_root)
        new_root.mainloop()
        
    def reset_colors(self):
        for node in self.vertices:
            self.update_node_color(node, 'white')

    def start_clicked(self):
        if not self.a_star_running and not self.search_successful:
            self.a_star_running = True
            self.a_star_search()

    def heuristic(self, node, target):
        x1, y1 = self.vertices[node]
        x2, y2 = self.vertices[target]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def a_star_search(self):
        # Get start and search nodes
        start_node = self.start_node_entry.get()
        search_node = self.search_node_entry.get()

        # Check if the start and search nodes are valid
        if start_node not in self.vertices or search_node not in self.vertices:
            self.status_label.config(text="Invalid start or search node!", font=("Times New Roman", 16, "bold", "italic"))
            return

        start_time = time.time()

        self.open_set.put((0, start_node, []))  # Initial state: (priority, node, path)
        while not self.open_set.empty():
            priority, current_node, path = self.open_set.get()

            # Check if the current_node matches the search_node (goal node)
            if current_node == search_node:
                self.search_successful = True
                self.start.config(state=tk.DISABLED)
                path.append(current_node)  # Include the goal node in the path
                end_time = time.time()
                path_cost = sum(graph.graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
                
                # Update the status label with the complete path information
                self.status_label.config(
                    text=f"Node {search_node} found! Path: {path}, Path Cost: {path_cost}, Time: {end_time - start_time:.2f} seconds",
                    font=("Times New Roman", 16, "bold", "italic"))
                
                # Update the color of the goal node
                self.update_node_color(search_node, 'green')
                self.a_star_running = False
                return

            if current_node not in self.closed_set:
                self.closed_set.add(current_node)
                self.update_node_color(current_node, 'green')
                for neighbor, weight in graph.graph[current_node].items():
                    if neighbor not in self.closed_set:
                        new_path = path + [current_node]
                        priority = len(new_path) + self.heuristic(neighbor, search_node) + weight
                        self.open_set.put((priority, neighbor, new_path))

            time.sleep(1 / self.speed_var.get())  # Adjust speed
            self.master.update()

        self.status_label.config(text=f"Node {search_node} not found!", font=("Times New Roman", 16, "bold", "italic"))
        self.a_star_running = False

def main():
    root = tk.Tk()
    app = AStarApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()