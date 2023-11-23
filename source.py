import math
from classes import Node, Arc
import matplotlib.pyplot as plt
import folium

personal_location = [47.060170774053, 15.462403989184102]


# Calculate the closest node to a certain location. First parameter in list is phi, second one is lambda
def find_closest_node(location: list[2]):
    min_dist = float('inf')
    closest_index = None

    with open('./data/nodepl.txt', 'r') as file:
        lines = file.readlines()

        for i, line in enumerate(lines):
            parts = line.strip().split()
            node_phi = float(parts[0])
            node_lambda = float(parts[1])

            distance = math.sqrt((location[0] - node_phi) ** 2 + (location[1] - node_lambda) ** 2)

            if distance < min_dist:
                min_dist = distance
                closest_index = i + 1

    return closest_index


# implementation of the except function for dictionaries: X \ {}
def dict_except(dict, element_to_remove):
    return {key: value for key, value in dict.items() if key != element_to_remove}


# return the node with the smallest label
def get_node_with_min_label(T: list[Node]) -> Node:
    min_node = T[0]
    for node in T:
        if node.label < min_node.label:
            min_node = node
    return min_node


def get_shortest_path(end: Node) -> list[Node]:
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = current.predecessor

    path.reverse()
    return path


# draw the path on the map
def plot_path(path: list[Node], name: str):

    # convert the list of nodes into a list of coordinate tuples
    new_path = []
    for node in path:
        new_path.append(node.coordinates)

    #setup folium
    map = folium.Map(location=[47.06865735508972, 15.440869640134975], zoom_start=15)

    folium.PolyLine(new_path, color='red', weight=10, opacity=1).add_to(map)

    map.save('./results/' + name + '.html')


########################################################################################################################
# create the set of all nodes
########################################################################################################################
V = {}
with open('./data/nodepl.txt', 'r') as file:
    lines = file.readlines()
    number_of_nodes = len(lines)
    for node in range(1, number_of_nodes + 1):
        coord = lines.pop(0).split()
        V[node] = Node(node, (float(coord[0]), float(coord[1])))
    del node

########################################################################################################################
# calculate the number of outgoing edges
########################################################################################################################
with open('./data/nodelist.txt', 'r') as file:
    lines = file.readlines()
    node_list = [None]  # set index 0 to None so the lists starts with one
    for line in lines:
        node_list.append(int(line.strip()))
    del line

for node in range(1, number_of_nodes + 1):
    V[node].num_arcs = node_list[node + 1] - node_list[node]
del node

########################################################################################################################
# add the arcs to the nodes
########################################################################################################################
# first read all lines of the arclist
with open('./data/arclist.txt', 'r') as file:
    lines = file.readlines()

# iterate through arclist and add the arcs to the nodes
for node in range(1, number_of_nodes + 1):
    for arc in range(V[node].num_arcs):
        current = lines.pop(0).split()
        index = int(current[0])
        time = float(current[1])
        distance = float(current[2])
        speed_limit = int(current[3])
        clazz = int(current[4])
        flags = int(current[5])
        V[node].add_arc(Arc(index, time, distance, speed_limit, clazz, flags))


########################################################################################################################
# Dijkstra’s routing algorithm
########################################################################################################################
def dijkstra(V: dict[int, Node], cost_model, vs: int, destination_index) -> list[Node]:
    # initialize variables
    T = []
    P = []

    # algorithm
    V[vs].label = 0
    T.append(V[vs])
    while len(T) > 0:
        v_i = get_node_with_min_label(T)
        P.append(v_i)
        T.remove(v_i)
        for arc_j in v_i.arcs:
            v_j = V[arc_j.target_node]
            if cost_model == 'distance':
                cost = arc_j.distance
            elif cost_model == 'time':
                cost = arc_j.time
            else:
                cost = arc_j.time

            if T.count(v_j) == 0 and P.count(v_j) == 0:
                v_j.label = v_i.label + cost
                v_j.predecessor = v_i
                T.append(v_j)
            if T.count(v_j) > 0 and v_i.label + cost < v_j.label:
                v_j.label = v_i.label + cost
                v_j.predecessor = v_i

    return get_shortest_path(V[destination_index])


basilika_path_distance = dijkstra(V, 'distance', find_closest_node(personal_location), 9328)
basilika_path_time = dijkstra(V, 'time', find_closest_node(personal_location), 9328)
eggenberg_path_distance = dijkstra(V, 'distance', find_closest_node(personal_location), 6031)
eggenberg_path_time = dijkstra(V, 'time', find_closest_node(personal_location), 6031)
murpark_path_distance = dijkstra(V, 'distance', find_closest_node(personal_location), 8543)
murpark_path_time = dijkstra(V, 'time', find_closest_node(personal_location), 8543)

plot_path(basilika_path_distance, 'basilika_distance')
plot_path(basilika_path_time, 'basilika_time')
plot_path(eggenberg_path_distance, 'eggenberg_distance')
plot_path(eggenberg_path_time, 'eggenberg_time')
plot_path(murpark_path_distance, 'murpark_distance')
plot_path(murpark_path_time, 'murpark_time')
