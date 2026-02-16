import os
import random
import time
import sys
import curses

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

class Tetris:
    def __init__(self, screen):
        self.screen = screen
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_shape = self.get_new_shape()
        self.current_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0
        self.score = 0
        self.game_over = False

    def get_new_shape(self):
        return random.choice(SHAPES)

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def valid_move(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell and (x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or self.grid[y + i][x + j]):
                    return False
        return True

    def place_shape(self, shape, x, y):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[y + i][x + j] = cell

    def clear_lines(self):
        new_grid = [row for row in self.grid if 0 in row]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        self.grid = [[0] * GRID_WIDTH for _ in range(lines_cleared)] + new_grid
        self.score += lines_cleared * 100

    def draw_grid(self):
        self.screen.clear()
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    self.screen.addch(y, x, '#')
        self.screen.addstr(GRID_HEIGHT + 1, 0, f"Score: {self.score}")
        self.screen.refresh()

    def game_loop(self):
        while not self.game_over:
            self.draw_grid()
            key