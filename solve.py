def random(graph):

    #Returns list of nodes, list of connections

    nodes = [graph.start]
    conns = []

    while nodes[-1] != graph.end:
        conns.append(random.choice(node.connections))
        if conns[-1].nodes[0] == graph.nodes[-1]:
            nodes.append(conns[-1].nodes[1])

        elif conns[-1].nodes[1] == graph.nodes[-1]:
            nodes.append(conns[-1].nodes[1])

    return (nodes, conns)

