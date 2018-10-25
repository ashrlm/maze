import img_parse
import solve

import sys
import argparse

maze_path = None
parser = argparse.ArgumentParser(description="Solve a given maze")
parser.add_argument('-m', help='Path of maze to solve')

args = parser.parse_args(sys.argv[1:])
maze_path = args.m

maze = img_parse.parse(maze_path)
