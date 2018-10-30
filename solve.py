import random

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