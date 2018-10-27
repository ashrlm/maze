#!/usr/bin/env python3

import img_parse
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