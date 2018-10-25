import random

def random_move(graph):

    curr_node = graph.start
    conns = []

    while curr_node != graph.end:
        conns.append(random.choice(curr_node.connections)) #Move randomly
        if conns[-1].nodes[0] == curr_node: #Check which one index of the conn our node is at
            curr_node = conns[-1].nodes[1] #Use different node - Movement

        elif conns[-1].nodes[1] == curr_node:
            curr_node = conns[-1].nodes[0]

    return conns