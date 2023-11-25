import pygame


class Agent:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def draw(self, screen, cell_width, cell_height):
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        pygame.draw.circle(
            screen,
            RED,
            ((self.start[1] + 1) * cell_width - cell_width // 2, self.start[0] * cell_height + cell_height // 2),
            min(cell_width, cell_height) // 3
        )

        pygame.draw.circle(
            screen,
            GREEN,
            ((self.goal[1] + 1) * cell_width - cell_width // 2, self.goal[0] * cell_height + cell_height // 2),
            min(cell_width, cell_height) // 3
        )
