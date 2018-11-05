#!/usr/bin/env python3

import img
import solve

import sys
import argparse

def parse_args():
    maze_path = None
    parser = argparse.ArgumentParser(description="Solve a given maze")
    parser.add_argument('-m', help='Path of maze to solve')
    parser.add_argument('-a', help="Algorithm to use for solving")
    parser.add_argument('-d', help='Directions if using dir_pri mode')

    parsed = {}

    args = parser.parse_args(sys.argv[1:])
    if args.m:
        parsed['m'] = args.m.lower()
    else:
        raise ValueError('Maze path required')
    if args.a:
        parsed['a'] = args.a.lower()
        if args.a == 'dir_pri':
            if args.d:
                parsed['d'] = args.d.lower()
            else:
                parsed['d'] = 'dlur'

    else:
        raise ValueError('Algorithm Required')

    return parsed

def __main__():
    parsed = parse_args()
    maze = img.parse(parsed['m'])
    if parsed['a'] == 'random_move':
        solved = solve.random_move(maze)

    elif parsed['a'] == 'dir_pri':
        solved = solve.dir_pri(maze, parsed['d'])

    elif parsed['a'] == 'dfs':
        solved = solve.dfs(maze)

    else:
        raise ValueError('Unknown Algorithm (random_move, dir_pri, dfs)')

    img.write_solution(solved, parsed['m'], maze)

if __name__ == '__main__':
    __main__()