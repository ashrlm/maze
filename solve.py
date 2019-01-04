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

    conn_rm_data_x = sorted((
        conn_rm.nodes[0].x,
        conn_rm.nodes[1].x
    ))
    conn_rm_data_y = sorted((
        conn_rm.nodes[0].y,
        conn_rm.nodes[1].y
    ))

    for conn in conns:

        conn_data_x = sorted((
            conn.nodes[0].x,
            conn.nodes[1].x
        ))
        conn_data_y = sorted((
            conn.nodes[0].y,
            conn.nodes[1].y
        ))

        if (conn_data_x, conn_data_y) == (conn_rm_data_x, conn_rm_data_y):
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

def dijkstra(graph): #BUG: This will fail for certain mazes (Decided 1515 is unsolvable, hangs on 7070)
    curr_node = graph.start
    curr_node.previous = []

    for node in graph.nodes: #Setup costs of nodes
        node.cost = float('inf')
        node.avaliable = list(node.connections)
    graph.start.cost = 0

    while curr_node.y != graph.end.y:

        while len(curr_node.avaliable) == 0:
            next_node = curr_node
            while len(next_node.avaliable) == 0:
                next_node = next_node.previous.pop()
                if len(next_node.avaliable) > 0:
                    old_node = curr_node
                    curr_node = next_node
                    break

            rm_conn(old_node.avaliable, img.Connection(
                (curr_node,
                old_node),
                0 #Distance does not matter
            ))
            rm_conn(curr_node.avaliable, img.Connection(
                (old_node,
                curr_node),
                0 #Distance does not matter
            ))

        min_cost = float('inf')
        min_node = None

        for conn in curr_node.avaliable: #Loop over all possible
            if (conn.nodes[0].x, conn.nodes[0].y) == (curr_node.x, curr_node.y):
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

        new_node = copy.copy(min_node)
        new_node.previous = curr_node.previous
        new_node.previous.append(curr_node)

        tmp_conn = img.Connection((new_node, curr_node), 0)
        rm_conn(curr_node.avaliable, tmp_conn)
        rm_conn(new_node.avaliable, tmp_conn)

        curr_node = new_node

    conns = [img.Connection((curr_node.previous[-1], graph.end), 0)]
    prev_node = graph.end
    for node in curr_node.previous:
        if node:
            conns.append(img.Connection((node, prev_node), 0))
            prev_node = node

    return conns
