import pygame


class Agent:
    def __init__(self, start, goal, cell_width, cell_height):
        self.position = start
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

    def move_up(self):
        self.position = (self.position[0] - 1, self.position[1])

    def move_down(self):
        self.position = (self.position[0] + 1, self.position[1])

    def move_left(self):
        self.position = (self.position[0], self.position[1] - 1)

    def move_right(self):
        self.position = (self.position[0], self.position[1] + 1)


