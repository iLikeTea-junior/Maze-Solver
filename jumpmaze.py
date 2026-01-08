
import random
import time
import math
import colorama
import heapq


def generate_maze(size=24, seed=None):
    """Create a new random maze to be solved.

    Args:
        size (int): The width and height of the maze.
        seed (int): The random seed; when create_maze is called twice with the same size and seed,
            the exact same maze list will be returned.

    Returns:
        A two dimensional list of heights associated with the squares, order `[row][column]`. When
        the height is `0`, there is a blocking element in this square.
    """
    if seed is not None:
        random.seed(seed)

    squares = []
    
    for _ in range(size):
        row = []
        for _ in range(size):
            row.append(random.randint(1, size**2) if random.randint(0, 4) else 0)
        squares.append(row)

    # Make sure the start and end squares are not blocked
    squares[0][0] = 1
    squares[-1][-1] = 2

    return squares


def print_maze(squares, path=None, show_heights=False):
    """Print a (solved) maze to the terminal.

    Args:
        squares (list(list(int))): The maze.
        path (list(tuple)): An optional list of (x,y) tuples that forms a path to be shown.
        show_heights (boolean): Show the height for each square. This makes the printed maze a lot wider.
    """

    size = len(squares)
    height_chars = math.ceil(math.log10(size**2))

    reset = colorama.Style.RESET_ALL
    print(reset)
    for y, row in enumerate(squares):
        for x, height in enumerate(row):

            if height == 0:
                color = colorama.Back.RED + colorama.Fore.BLACK
            elif path is not None and (x, y) in path:
                color = colorama.Back.GREEN + colorama.Fore.BLACK
            else:
                color = colorama.Back.BLACK + colorama.Fore.WHITE

            if show_heights:
                number_str = (f"%0{height_chars}d" % height) if height else (" " * height_chars)
                print(f"{color}{number_str}{reset} ", end="")
            else:
                print(f"{color} ", end="")
        print(reset)
    print("")


def demo(size=24, seed=None, jumps=False):
    """Generates a maze, solves it and prints the results.

    Args:
        size (int): Width and height of the maze to demo.
        seed (int): Random seed of the maze to generate.
        jumps (boolean): Allow jumps between squares with the same height.
    """

    if seed is None:
        seed = int(time.perf_counter()) % 10000

    print(f"Solving {size}x{size} seed {seed} {'with' if jumps else 'without'} jumps...")

    maze = generate_maze(size, seed)

    start_time = time.perf_counter()
    path = solve(maze, jumps)
    elapsed = time.perf_counter() - start_time

    if size <= 100:
        print_maze(maze, path, size <= 24)

    if path:
        print(f"Cheapest path: {path} (length {len(path)})")
    else:
        print("No path found")
        
    print(f"Solver took {round(elapsed, 3)}s\n\n\n")


def solve(maze, jumps=False):
    """Calculate the cheapest (in terms of meters climbed) path for a maze.

    Args:
        maze (list(list(int))): The maze.

    Returns:
        The cheapest path as a list of (x,y) tuples, starting with the top left
        corner (0,0) and ending with the lower right corner (N-1, N-1).
        If no path exists, `None` is returned.
    """
    origin = (0, 0)
    width, height = len(maze[0]), len(maze)
    destination = (width-1), (height-1) # x, y

    min_heap = [(0, maze[0][0], origin)]
    visited = set()
    path_traces: dict[tuple[int, int], tuple[int, None | tuple[int, int]]] = {origin: (0, None)}
    jumping_neighbors = {}
    if jumps:
        jumping_neighbors.update(get_more_neighbors(maze))

    while min_heap:
        height_progress, cur_height, cur_coord = heapq.heappop(min_heap)

        if cur_coord == destination:
            break
        if cur_coord in visited:
            continue

        cliffs = get_neighbors(cur_coord, width, height, maze)
        if jumps:
            cliffs.extend(jumping_neighbors.get(cur_height)) # type: ignore

        for cliff_coord, cliff_height in cliffs:
            if jumps and cliff_coord == cur_coord:
                continue

            total_height = max(0, cliff_height - cur_height) + height_progress
            heapq.heappush(min_heap, (total_height, cliff_height, cliff_coord))

            if cliff_coord not in path_traces or path_traces[cliff_coord][0] > total_height:
                path_traces[cliff_coord] = (total_height, cur_coord)
        visited.add(cur_coord)

    if destination not in path_traces:
        return None
    
    path = [destination]
    while destination != origin:
        destination = path_traces[destination][1] # type: ignore
        path.insert(0, destination) # type: ignore

    return path


def get_neighbors(current_coord, maze_w, maze_h, maze):
    x, y = current_coord
    up, right, down, left = (x, y-1), (x+1, y), (x, y+1), (x-1, y)
    neighbors = []

    for current_x, current_y in [up, right, down, left]:
        if 0 <= current_x < maze_w and 0 <= current_y < maze_h and maze[current_y][current_x] != 0:
            neighbors.append(((current_x, current_y), maze[current_y][current_x]))

    return neighbors


def get_more_neighbors(maze):
    same_neighbors = {}

    for y, row in enumerate(maze):
        for x, value in enumerate(row):
            if value not in same_neighbors and value != 0:
                same_neighbors[value] = [((x, y), value)]
            elif value in same_neighbors and value != 0:
                same_neighbors[value].append(((x, y), value))

    return same_neighbors


if __name__ == "__main__":
    print("------ Solvable mazes, without teleports ------\n")
    demo(3, 7)
    demo(4, 2)
    demo(7, 2)
    demo(10, 3)
    demo(24, 1)
    demo(100, 1)
    demo(250, 1)
    demo(1000, 1)

    print("------ Unsolvable mazes, without teleports ------\n")
    demo(3, 20)
    demo(24, 126)

    print("------ Solvable mazes, with teleports ------\n")
    demo(10, 39047, True)
    demo(24, 3305, True)
    demo(100, 595, True)
    demo(1000, 129, True)
