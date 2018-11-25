import random
import img
import copy

def conn_node(conn, node):
    if conn.nodes[0] == node: #Check which one index of the conn our node is at
        return conn.nodes[1] #Use different node - Movement

    elif conn.nodes[1] == node:
        return conn.nodes[0]

def random_move(graph):

    # This will move completely randomly - Testing only

    curr_node = graph.start
    conns = []

    while curr_node != graph.end:
        conns.append(random.choice(curr_node.connections)) #Move randomly
        curr_node = conn_node(conns[-1], curr_node)

    return conns

def dir_pri(graph, pri='ldru'): #Pri - Str some permutation of udlr (Up, Down, Left, Right)

    curr_node = graph.start
    conns = []
    prev_dir = 'u'

    def expand_node(node, prev_dir):

        for dir in pri.replace(prev_dir, ''):
            for conn in node.connections:
                if dir == 'u':
                    if conn_node(conn, node).y < node.y:
                        return (conn_node(conn, node), conn)
                if dir == 'd':
                    if conn_node(conn, node).y > node.y:
                        return (conn_node(conn, node), conn)
                if dir == 'l':
                    if conn_node(conn, node).x < node.x:
                        return (conn_node(conn, node), conn)
                if dir == 'r':
                    if conn_node(conn, node).x > node.x:
                        return (conn_node(conn, node), conn)

        # No alternative - Rerun allowing backtrack
        for dir in pri:
            for conn in node.connections:
                if dir == 'u':
                    if conn_node(conn, node).y < node.y:
                        return (conn_node(conn, node), conn)
                if dir == 'd':
                    if conn_node(conn, node).y > node.y:
                        return (conn_node(conn, node), conn)
                if dir == 'l':
                    if conn_node(conn, node).x < node.x:
                        return (conn_node(conn, node), conn)
                if dir == 'r':
                    if conn_node(conn, node).x > node.x:
                        return (conn_node(conn, node), conn)

    while curr_node != graph.end:
        expanded = expand_node(curr_node, prev_dir)

        if expanded[0].x < curr_node.x:
            prev_dir = 'r'
        elif expanded[0].x > curr_node.x:
            prev_dir = 'l'
        elif expanded[0].y < curr_node.y:
            prev_dir = 'd'
        elif expanded[0].y > curr_node.y:
            prev_dir = 'u'

        curr_node = expanded[0]
        conns.append(expanded[1])

    return conns


def dfs(graph):

    def conn_filter(conns_old):
        conns = list(conns_old) #Create copy for returning

        for i, conn in enumerate(conns_old[:-1]):

            if not (conn.nodes[0] in conns_old[i+1].nodes or conn.nodes[1] in conns_old[i+1].nodes): #Missing Connection
                if conn.nodes[0].x == conns_old[i+1].nodes[0].x: #Same x - Missing Y CONN
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[0].y-conns_old[i+1].nodes[0].y)
                    ))

                if conn.nodes[0].x == conns_old[i+1].nodes[1].x:
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[0].y-conns_old[i+1].nodes[1].y)
                    ))

                if conn.nodes[1].x == conns_old[i+1].nodes[0].x:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[1].y-conns_old[i+1].nodes[0].y)
                    ))

                if conn.nodes[1].x == conns_old[i+1].nodes[1].x:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[1].y-conns_old[i+1].nodes[1].y)
                    ))

                if conn.nodes[0].y == conns_old[i+1].nodes[0].y:
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[0].x-conns_old[i+1].nodes[0].x)
                    ))

                if conn.nodes[0].y == conns_old[i+1].nodes[1].y:
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[0].x-conns_old[i+1].nodes[1].x)
                    ))

                if conn.nodes[1].y == conns_old[i+1].nodes[0].y:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[1].x-conns_old[i+1].nodes[0].x)
                    ))

                if conn.nodes[1].y == conns_old[i+1].nodes[1].y:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[1].x-conns_old[i+1].nodes[1].x)
                    ))

        for conn in conns:
            tmp = list(conns) #Create temp to play with without altering conns
            tmp.remove(conn)
            for conn_ in tmp:
                if conn_.nodes in (conn.nodes, conn.nodes[::-1]):
                    if conn in conns:
                        conns.remove(conn)

        return conns

    node_conns = {graph.start: Connection((graph.start, graph.start), 0)}
    # Format for above - {Node, Conn leading to node}

    while list(node_conns.keys())[-1] != graph.end:
        if not hasattr(list(node_conns.keys())[-1], 'avaliable'):
            list(node_conns.keys())[-1].avaliable = list(node_conns.keys())[-1].connections
        try:
            list(node_conns.keys())[-1].avaliable.remove(list(node_conns.values())[-2])
        except:
            pass

        for conn in list(node_conns.keys())[-1].avaliable: #Filter out ones we've already been to
            if conn in list(node_conns.values()):
                list(node_conns.keys())[-1].avaliable.remove(conn)

        if len(list(node_conns.keys())[-1].avaliable) == 0:
            try:
                list(node_conns.keys())[-2].avaliable.remove(list(node_conns.values())[-1])
            except (IndexError, ValueError):
                pass

            del node_conns[list(node_conns.keys())[-1]]
            continue

        next_conn = random.choice(list(node_conns.keys())[-1].avaliable)
        list(node_conns.keys())[-1].avaliable.remove(next_conn)
        node_conns[conn_node(next_conn, list(node_conns.keys())[-1])] = next_conn #Get next node, add to dict with val of next_conn

    return conn_filter(list(node_conns.values())) #Only return filtered connections

def rm_conn(conns, conn_rm):
    for conn in conns:
        if conn.nodes in (conn_rm.nodes, conn_rm.nodes[::-1]):
            try:
                conns.remove(conn)
            except ValueError:
                pass

def dfs(graph):

    nodes = [graph.start]
    conns = []

    for node in graph.nodes: #Setup av_dir for node
        node.avaliable = list(node.connections)

    while nodes[-1] != graph.end:

        if nodes[-1].avaliable == []:
            nodes.pop()
            conns.pop()
            continue

        for conn in nodes[-1].avaliable:
            if conn.nodes[0] == nodes[-1]:
                conns.append(conn)
                rm_conn(nodes[-1].avaliable, conn)
                rm_conn(conn.nodes[1].avaliable, conn)
                nodes.append(conn.nodes[1])
                break

            else:
                conns.append(conn)
                rm_conn(nodes[-1].avaliable, conn)
                rm_conn(conn.nodes[0].avaliable, conn)
                nodes.append(conn.nodes[0])
                break

    return conns

 # TODO: Rewrite dijkstra
 # Required: Store .previous as a list allowing it to backtrack multiple at once, skipping Nones, to prevent None Error
 # Methodology: Start at Start, check to backtrack, loop over all in avaliable, add/update cost/previous of each, go to nearest one, loop

def dijkstra(graph):
    curr_node = graph.Start

    for node in graph.nodes: #Setup costs of nodes
        node.cost = float('inf')
    graph.start.cost = 0

    while curr_node != graph.end:

        if curr_node.avaliable == []:
            pass #TODO: Backtrack

        min_cost = float('inf')
        min_node = None

        for conn in curr_node.avaliable: #Loop over all possible
            if conn.nodes[0] == curr_node:
                if curr_node.cost + conn.cost < conn.nodes[1].cost:
                    conn.nodes[1].cost = curr_node.cost + conn.cost #Update cost - swapping

                if conn.nodes[1].cost < min_cost:
                    min_cost = conn.nodes[1].cost #Update min_cost to get nearest node
                    min_node = conn.nodes[1] #Update next node

            else:
                if curr_node.cost + conn.cost < conn.nodes[1].cost:
                    conn.nodes[0].cost = curr_node.cost + conn.cost #Update cost - swapping

                if conn.nodes[0].cost < min_cost:
                    min_cost = conn.nodes[0].cost #Update min_cost to get nearest node
                    min_node = conn.nodes[0] #Update next node

        new_node = copy.deepcopy(min_node) #TODO: Copy this instead of creating ref
        new_node.previous = curr_node.previous
        new_node.previous.append(curr_node)
        curr_node = new_node

    conns = []
    for node in graph.end.previous:
        if node:
            conns.append(img.Connection((node, graph.end), 0))

    return conns