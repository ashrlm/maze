import random

def random_move(graph):

    curr_node = graph.start
    conns = []

    while curr_node != graph.end:
        conns.append(random.choice(curr_node.connections))
        if conns[-1].nodes[0] == curr_node:
            curr_node = conns[-1].nodes[1]

        elif conns[-1].nodes[1] == curr_node:
            curr_node = conns[-1].nodes[0]

    return conns