class Arc:
    def __init__(self, target_node, time, distance, speed_limit, clazz, flags):
        self.target_node = target_node
        self.time = time
        self.distance = distance
        self.speed_limit = speed_limit
        self.clazz = clazz
        self.flags = flags


class Node:
    def __init__(self, index, coordinates):
        self.label = float('inf')
        self.arcs = []
        self.num_arcs = 0
        self.predecessor = None
        self.index = index
        self.coordinates = coordinates

    def add_arc(self, arc: Arc):
        self.arcs.append(arc)

    def __str__(self):
        arcs_str = ", ".join(f"({arc.target_node.label}, {arc.cost})" for arc in self.arcs)
        return f"Node {self.label} with {self.num_arcs} arcs: {arcs_str}"
