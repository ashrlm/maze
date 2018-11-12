#!/usr/bin/env python3

import solve
import img

import sys
import argparse
import subprocess

import argparse

def parse_args():
    maze_path = None
    parser = argparse.ArgumentParser(description="Solve a given maze")
    parser.add_argument('-s', help='Size of maze to generate. (Also cue for generation)')
    parser.add_argument('-m', help='Path of maze to solve')
    parser.add_argument('-a', help="Algorithm to use for solving")
    parser.add_argument('-d', help='Directions if using dir_pri mode')

    parsed = {}

    args = parser.parse_args(sys.argv[1:])
    if args.s:
        parsed['s'] = args.s
        return parsed
    if args.m:
        parsed['m'] = args.m
    else:
        raise ValueError('Maze path required')
    if args.a:
        parsed['a'] = args.a
        if args.a == 'dir_pri':
            if args.d:
                parsed['d'] = args.d
            else:
                parsed['d'] = 'dlur'

    else:
        raise ValueError('Algorithm Required')

    return parsed

def __main__():
    parsed = parse_args()
    try:
        size = parsed['s']
        img.generate(size)
        print("Maze of size", s, "generated.")
        quit
    except KeyError:
        pass
    maze = img.parse(parsed['m'])
    if parsed['a'] == 'random_move':
        solved = solve.random_move(maze)

    elif parsed['a'] == 'dir_pri':
        solved = solve.dir_pri(maze, parsed['d'])

    elif parsed['a'] == 'dfs':
        solved = solve.dfs(maze)

    elif parsed['a'] == 'dijkstra':
        solved = solve.dijkstra(maze)

    img.write_solution(solved, parsed['m'], maze)

if __name__ == '__main__':
    __main__()
