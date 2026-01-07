from jumpmaze import solve
import random
import unittest
from unittest.mock import patch


class FunctionsTest(unittest.TestCase):

    def test_solve_maze_width_different_width_and_height(self):
        without_jumps = ([[random.randint(1, 100), random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)] for _ in range(3)], False)
        with_jumps = ([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], True)

        cases = [without_jumps, with_jumps]

        for maze, jump in cases:
            result = solve(maze, jump)
            self.assertTrue(result, "No path was found! The algorithm apparently only handles same with and height")

    def test_solve_maze_with_only_walls(self):
        without_jumps = ([[0, 0, 0] for _ in range(3)], False)
        with_jumps = ([[0, 0, 0] for _ in range(3)], True)

        cases = [without_jumps, with_jumps]

        for maze, jumps in cases:
            result = solve(maze, jumps)
            self.assertIsNone(result, "Returns a path even though the maze is completely full of walls.")

    def test_solve_empty_maze(self):
        without_jumps = ([[]], False)
        with_jumps = ([[]], True)

        cases = [without_jumps, with_jumps]

        for maze, jumps in cases:
            result = solve(maze, jumps)
            self.assertIsNone(result, "Returns a path al though there is no maze.")

    def test_solve_one_destination_only(self):
        without_jumps = ([[1]], False)
        with_jumps = ([[1]], True)

        cases = [without_jumps, with_jumps]

        for maze, jumps in cases:
            result = solve(maze, jumps)
            self.assertIsNotNone(result, "Gives no result despite having only one destination.")


if __name__ == "__main__":
    unittest.main()
