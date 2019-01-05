#!/usr/bin/env python3

import solve
import img
from generate import Generate

import sys
import argparse
import subprocess

def parse_args():
    maze_path = None
    parser = argparse.ArgumentParser(description="Solve a given maze")
    parser.add_argument('-size', help='Size of maze to generate. (Also cue for generation)')
    parser.add_argument('-maze', help='Path of maze to solve')
    parser.add_argument('-algorithm', help="Algorithm to use for solving")
    parser.add_argument('-dir_pri', help='Directions if using dir_pri mode')

    parsed = {}

    args = parser.parse_args(sys.argv[1:])
    if args.size:
        parsed['s'] = int(args.size)
        return parsed
    if args.maze:
        parsed['m'] = args.maze.lower()
    else:
        raise ValueError('Maze path required')
    if args.algorithm:
        parsed['a'] = args.algorithm.lower()
        if args.algorithm == 'dir_pri':
            if args.dir_pri:
                parsed['d'] = args.dir_pri.lower()
            else:
                parsed['d'] = 'dlur'

    else:
        raise ValueError('Algorithm Required')

    return parsed

def main():
    parsed = parse_args()
    try:
        size = parsed['s']
        Generate.generate(size)
        quit()

    except KeyError:
        pass
    maze = img.parse(parsed['m'])
    if parsed['a'] == 'random_move':
        try:
            solved = solve.random_move(maze)
        except IndexError:
            print("Unsolvable maze")
            quit()

    elif parsed['a'] == 'dir_pri':
        try:
            solved = solve.dir_pri(maze, pri=parsed['d'])
        except TypeError:
            print("Unsolvable maze")
            quit()

    elif parsed['a'] == 'dijkstra':
        try:
            solved = solve.dijkstra(maze)
        except IndexError:
            print("Unsolvable maze")
            quit()

    elif parsed['a'] == 'dfs':
        try:
            solved = solve.dfs(maze)
        except IndexError:
            print("Unsolvable maze")
            quit()

    else:
        raise ValueError('Unknown Algorithm (random_move, dir_pri, dfs, dijkstra)')

    img.write_solution(solved, parsed['m'], maze)

if __name__ == '__main__':
    main()
