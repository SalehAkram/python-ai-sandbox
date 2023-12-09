import pygame
import random


class Agent:
    def __init__(self, start, goal, cell_width, cell_height):
        self.position = start
        self.start = start
        self.goal = goal
        self.radius = min(cell_width, cell_height) // 6
        self.steps_taken = 0
        self.is_alive = True

    def think(self, maze):
        movements = [self.move_up, self.move_down, self.move_left, self.move_right]
        random_movement = random.choice(movements)
        random_movement(maze)

    def draw(self, screen, cell_width, cell_height):
        red = (255, 0, 0)
        pygame.draw.circle(
            screen,
            red,
            ((self.position[1] + 1) * cell_width - cell_width // 2, self.position[0] * cell_height
             + cell_height // 2),
            self.radius  # Use precomputed radius here
        )

    def move(self, maze, next_position):
        # Check if the next move is within bounds and not colliding with a wall
        next_row, next_col = next_position

        if 0 <= next_row < len(maze.cells) and 0 <= next_col < len(maze.cells[0]):
            if maze.cells[next_row][next_col] == 0:
                self.position = next_position
                self.steps_taken += 1
                return

        self.is_alive = False

    def move_up(self, maze):
        next_position = (self.position[0] - 1, self.position[1])
        self.move(maze, next_position)

    def move_down(self, maze):
        next_position = (self.position[0] + 1, self.position[1])
        self.move(maze, next_position)

    def move_left(self, maze):
        next_position = (self.position[0], self.position[1] - 1)
        self.move(maze, next_position)

    def move_right(self, maze):
        next_position = (self.position[0], self.position[1] + 1)
        self.move(maze, next_position)
