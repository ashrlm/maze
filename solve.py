import random
from img import Connection

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

                elif conn.nodes[0].x == conns_old[i+1].nodes[1].x:
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[0].y-conns_old[i+1].nodes[1].y)
                    ))

                elif conn.nodes[1].x == conns_old[i+1].nodes[0].x:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[1].y-conns_old[i+1].nodes[0].y)
                    ))

                elif conn.nodes[1].x == conns_old[i+1].nodes[1].x:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[1].y-conns_old[i+1].nodes[1].y)
                    ))

                elif conn.nodes[0].y == conns_old[i+1].nodes[0].y:
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[0].x-conns_old[i+1].nodes[0].x)
                    ))

                elif conn.nodes[0].y == conns_old[i+1].nodes[1].y:
                    conns.append(Connection(
                        (conn.nodes[0],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[0].x-conns_old[i+1].nodes[1].x)
                    ))

                elif conn.nodes[1].y == conns_old[i+1].nodes[0].y:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[0]),
                        abs(conn.nodes[1].x-conns_old[i+1].nodes[0].x)
                    ))

                elif conn.nodes[1].y == conns_old[i+1].nodes[1].y:
                    conns.append(Connection(
                        (conn.nodes[1],
                         conns_old[i+1].nodes[1]),
                        abs(conn.nodes[1].x-conns_old[i+1].nodes[1].x)
                    ))

        conns_clean = list(conns)
        for conn in conns:

            if conn not in conns_old:
                print(len(graph.img)-1, conn.nodes[0].x, conn.nodes[0].y, conn.nodes[1].x, conn.nodes[1].y)

                if len(graph.img) - 1 in (conn.nodes[0].y, conn.nodes[1].y):
                    conns_clean.remove(conn)

        return conns_clean


    node_conns = {graph.start: Connection((graph.start, graph.start), 0)}
    # Format for above - {Node, Conn leading to node}

    while list(node_conns.keys())[-1] != graph.end:

        if not hasattr(list(node_conns.keys())[-1], 'avaliable'):
            list(node_conns.keys())[-1].avaliable = list(node_conns.keys())[-1].connections

        for conn in list(node_conns.keys())[-1].avaliable: #Filter out ones we've already been to
            if conn in list(node_conns.values()):
                list(node_conns.keys())[-1].avaliable.remove(conn)

        if list(node_conns.keys())[-1].avaliable == []:
            try:
                list(node_conns.keys())[-2].avaliable.remove(list(node_conns.values())[-1])
            except ValueError:
                pass
            del node_conns[list(node_conns.keys())[-1]]
            continue

        next_conn = random.choice(list(node_conns.keys())[-1].avaliable)
        node_conns[conn_node(next_conn, list(node_conns.keys())[-1])] = next_conn #Get next node, add to dict with val of next_conn

    return conn_filter(list(node_conns.values())) #Only return connections