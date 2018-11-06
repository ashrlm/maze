# MazeSolve

### About
This program will take some maze and solve it.

### Usage
First, install `pipenv` with `python -m pip install pipenv`
Install all dependencies with `pipenv install`
To generate a maze, run `pipenv run python generate.py -s [SIZE]`
To solve a given maze, refer to the algorithm-specific instructions below

##### Avaliable Algorithms:
    - Random Walk - random_move
        - `pipenv python run main.py -m [path\to\maze.png] -a random_move`
    - Directional Prioritization - dir_pri:
        - `pipenv python run main.py -m [path\to\maze.png] -a dir_pri -d [directions]`
        - [directions] can be replaced with some string representing the order to check directions
            - U - Up
            - D - Down
            - L - Left
            - R - Right
            - Example: DLUR - Down, left, up, right
     - Depth-First Search - dfs:
        -  `pipenv run python main.py -m [path\to\maze.png] -a dfs`