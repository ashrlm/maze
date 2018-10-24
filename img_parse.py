#!/usr/bin/env python3

from PIL import Image

# TODO: Only create node when there is a new direction rhat previously wasnt present

class Node():

    nodes = []

    def __init__(self, xy, av_dirs):
        self.x, self.y = xy #XYPos - Used when drawing solution
        self.av_dirs = av_dirs # Avaliable Directions - Determine if others are nodes
        self.connections = []
        Node.nodes.append(self)

class Connection():
    def __init__(self, nodes, weight):
        self.nodes = nodes
        self.weight = weight

class Graph():
    def __init__(self, nodes, connections):
        self.nodes = nodes
        self.connections = connections

def get_av_dirs(img, xy):
    x,y = xy
    av_dirs = [False] * 4 #Up, Down, Left, Right

    if x > 0:
        if img[y][x-1] == (255, 255, 255):
            av_dirs[2] = True #Right
    if x < len(img[0]) - 2:
        if img[y][x+1] == (255, 255, 255):
            av_dirs[3] = True #Left
    if y > 0:
        if img[y-1][x] == (255, 255, 255):
            av_dirs[0] = True #Up

    if y < len(img) - 2:
        if img[y+1][x] == (255, 255, 255):
            av_dirs[1] = True #Down

    return av_dirs

def is_conn(img, node, node_):

    if (node.x, node.y) == (node_.x, node_.y):
        return False #Same node


    if node.x == node_.x:
        for y in range(min(node.y, node_.y), max(node.y, node_.y)):
            if img[y][node.x] == (0, 0, 0):
                return False

        return True

    if node.y == node_.y:
        for x in range(min(node.x, node_.x), max(node.x, node_.x)):
            if img[node.y][x] == (0, 0, 0):
                return False

        return True

def is_node(img, xy):
    x,y = xy
    if img[y][x] == (255, 255, 255):

        if y in (0, len(img) - 1):
            return True

        av_dirs = get_av_dirs(img, xy)

        for i, dir in enumerate(av_dirs):
            if dir: # TODO: Code to check that node we gained direction from is not a node itself
                if x > 0 and img[y][x-1] == (255, 255, 255):
                    if not get_av_dirs(img, (x-1, y))[i]:
                        if av_dirs != get_av_dirs(img, (x+1, y)):
                            return True
                if x < len(img[0]) - 2 and img[y][x+1] == (255, 255, 255):
                    if not get_av_dirs(img, (x+1,y ))[i]:
                        if av_dirs != get_av_dirs(img, (x-1, y)):
                            return True
                if y > 0 and img[y-1][x] == (255, 255, 255):
                    if not get_av_dirs(img, (x, y-1))[i]:
                        if av_dirs != get_av_dirs(img, (x, y+1)):
                            return True
                if y < len(img) - 2 and img[y+1][x] == (255, 255, 255):
                    if not get_av_dirs(img, (x, y+1))[i]:
                        if av_dirs != get_av_dirs(img, (x, y-1)):
                            return True

def parse(img_path):
    img = Image.open(img_path)
    w, h = img.size

    pxs = list(img.getdata())
    pxs = [pxs[i:i + w] for i in range(0, len(pxs), w)] #Split list into nested lists

    connections = []

    for y, row in enumerate(pxs):
        for x, px in enumerate(row):
            if is_node(pxs, (x, y)):
                Node(
                    (x, y),
                    get_av_dirs(pxs, (x, y))
                )

    for i, node in enumerate(Node.nodes):
        for i_, node_ in enumerate(Node.nodes):
            if is_conn(pxs, node, node_):
                new_conn = Connection(
                    (node, node_),
                    abs(node.x - node_.x))

                node.connections.append(new_conn)

                for connection in connections:
                    if connection.nodes == new_conn.nodes[::-1]:
                        break

                else:
                    connections.append(new_conn)


    return Graph(Node.nodes, connections)