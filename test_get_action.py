import csv
import networkx as nx

def read_adjacency_matrix(file_path):
    adjacency_matrix = {}
    nodes = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            node_name = row[0]
            nodes.append(node_name)
            adjacency_matrix[node_name] = {row[i]: float(row[i+1]) for i in range(1, len(row), 2)}
                
            print(f"{node_name}: {adjacency_matrix[node_name]}")
    return adjacency_matrix,nodes

def find_shortest_path(adjacency_matrix, start_node, end_node):
    G = nx.Graph()

    for node, neighbors in adjacency_matrix.items():
        for neighbor, angle in neighbors.items():
            G.add_edge(node, neighbor, weight=1)
                
    try:
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node)
        shortest_path_cost = nx.shortest_path_length(G, source=start_node, target=end_node)
        return shortest_path_cost, shortest_path
    except nx.NetworkXNoPath:
        return float('inf'), []
    
def read_node_positions(file_path):
    node_positions = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            node_name, x, z, y, angle = row
            node_positions[node_name] = {'x': float(x), 'z': float(z), 'y': float(y), 'angle': float(angle)}
    return node_positions

def get_query(node_positions, shortest_path_nodes, adjacency_matrix):
    start_node = shortest_path_nodes[0]
    position = [node_positions[start_node]["x"], node_positions[start_node]["z"], node_positions[start_node]["y"]]
    print(position)
    print(node_positions[start_node]["angle"])
    
    actions = []
    values = []
    
    for i in range(len(shortest_path_nodes)):
        node = shortest_path_nodes[i]
        if node == shortest_path_nodes[-1]:
            actions.append("turn")
            values.append(node_positions[node]["angle"])
            actions.append("stop")
            break
        next_node = shortest_path_nodes[i+1]
        position = [node_positions[node]["x"], node_positions[node]["z"], node_positions[node]["y"]]
        if adjacency_matrix[node][next_node] != -1:
            actions.append("turn")
            values.append(adjacency_matrix[node][next_node])
            
        if (node_positions[node]["x"] != node_positions[next_node]["x"]) and (node_positions[node]["y"] != node_positions[next_node]["y"]):
            actions.append("warp")
        else:
            actions.append("change_goal")
            actions.append("go")
            
        values.append([node_positions[next_node]["x"], node_positions[next_node]["z"], node_positions[next_node]["y"]])
        
    return actions, values
    
    

if __name__ == "__main__":
    link_file_path = "data/scene_datasets/mp3d/2azQ1b91cZZ/2azQ1b91cZZ_link.csv"
    position_file_path = "data/scene_datasets/mp3d/2azQ1b91cZZ/2azQ1b91cZZ_position.csv"
    start_node = "7_wait_2"
    end_node = "0_wait_3"

    adjacency_matrix, nodes = read_adjacency_matrix(link_file_path)

    if start_node not in nodes or end_node not in nodes:
        print("Invalid node names.")
    shortest_path_cost, shortest_path_nodes = find_shortest_path(adjacency_matrix, start_node, end_node)
    if shortest_path_cost == float('inf'):
        print("No path found.")
    
    print(f"The shortest path from {start_node} to {end_node} is: {shortest_path_nodes}")
    print(f"The cost of the shortest path is: {shortest_path_cost}")
    
    node_positions = read_node_positions(position_file_path)
    actions, values = get_query(node_positions, shortest_path_nodes, adjacency_matrix)
    print(actions)
    print(values)
