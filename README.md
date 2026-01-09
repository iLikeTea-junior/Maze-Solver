# 🧩 Maze-Solver
This project implements a maze-solving algorithm.

The maze is represented as a square grid (same width and height).
Red squares represent blockades that can't be crossed.
All other squares contain a number representing the height in meters.

The goal is to find the easiest path from the top-left square to the
bottom-right square by minimizing the total climbing effort.
Only upward movement costs effort (the positive height difference);
moving downhill costs zero effort.

Maze generation and visualization were provided.
The task is to implement the solve(maze) function to compute the optimal path, and also make the unit test.


# 💻 Technologies
- Python


# 🧠 What I Learned
- Create a unit test to validate whether a module works as intended.
- implement algorithms expressed in pseudo-code.
- Select algorithms based on algorithmic time/space complexity.
- When to use arrays (lists), maps (dictionairies), linked lists and trees.
- Used sorted data structures such as trees and heaps.

# 🤔💭 What could be Improved
**1st** -> The solve function could be smaller. Python complains saying that it is to complex.

**2nd** -> The algorithm does not sovle 1000x1000 grid.
