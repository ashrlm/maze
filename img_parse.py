#!/usr/bin/env python3

from PIL import Image

# TODO: Only create node when there is a new direction rhat previously wasnt present

class Node():

    nodes = []

    def __init__(self, xy, av_dirs):
        self.xy = xy #XYPos - Used when drawing solution
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

def node(img, xy):
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
                            print(av_dirs, get_av_dirs(img, (x-1, y)), xy, 'l', i)
                            return True
                if x < len(img[0]) - 2 and img[y][x+1] == (255, 255, 255):
                    if not get_av_dirs(img, (x+1,y ))[i]:
                        if av_dirs != get_av_dirs(img, (x-1, y)):
                            print(av_dirs, get_av_dirs(img, (x+1, y)), xy, 'r')
                            return True
                if y > 0 and img[y-1][x] == (255, 255, 255):
                    if not get_av_dirs(img, (x, y-1))[i]:
                        if av_dirs != get_av_dirs(img, (x, y+1)):
                            print(av_dirs, get_av_dirs(img, (x, y-1)), xy, 'u')
                            return True
                if y < len(img) - 2 and img[y+1][x] == (255, 255, 255):
                    if not get_av_dirs(img, (x, y+1))[i]:
                        if av_dirs != get_av_dirs(img, (x, y-1)):
                            print(av_dirs, get_av_dirs(img, (x, y+1)), xy, 'd')
                            return True

def parse(img_path):
    img = Image.open(img_path)
    w, h = img.size

    pxs = list(img.getdata())
    pxs = [pxs[i:i + w] for i in range(0, len(pxs), w)] #Split list into nested lists

    connections = []

    for y, row in enumerate(pxs):
        for x, px in enumerate(row):
            if node(pxs, (x, y)):
                Node(
                    (x, y),
                    get_av_dirs(pxs, (x, y))
                )

    return Graph(Node.nodes, []) # TODO: Add Connection parsing

g=parse('imgs/1010.png')