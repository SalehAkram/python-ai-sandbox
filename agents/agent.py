import pygame


class Agent:
    def __init__(self, start, goal, cell_width, cell_height):
        self.position = start
        self.start = start
        self.goal = goal
        self.radius = min(cell_width, cell_height) // 6

    def draw(self, screen, cell_width, cell_height):
        red = (255, 0, 0)
        pygame.draw.circle(
            screen,
            red,
            ((self.position[1] + 1) * cell_width - cell_width // 2, self.position[0] * cell_height + cell_height // 2),
            self.radius  # Use precomputed radius here
        )

    def is_valid_move(self, maze, next_position):
        # Check if the next move is within bounds and not colliding with a wall
        next_row, next_col = next_position

        if 0 <= next_row < len(maze.cells) and 0 <= next_col < len(maze.cells[0]):
            if maze.cells[next_row][next_col] == 0:
                return True
        return False

    def move_up(self, maze):
        next_position = (self.position[0] - 1, self.position[1])
        if self.is_valid_move(maze, next_position):
            self.position = next_position
        else:
            self.position = self.start

    def move_down(self, maze):
        next_position = (self.position[0] + 1, self.position[1])
        if self.is_valid_move(maze, next_position):
            self.position = next_position
        else:
            self.position = self.start

    def move_left(self, maze):
        next_position = (self.position[0], self.position[1] - 1)
        if self.is_valid_move(maze, next_position):
            self.position = next_position
        else:
            self.position = self.start  # Reset to start position

    def move_right(self, maze):
        next_position = (self.position[0], self.position[1] + 1)
        if self.is_valid_move(maze, next_position):
            self.position = next_position
        else:
            self.position = self.start  # Reset to start position
