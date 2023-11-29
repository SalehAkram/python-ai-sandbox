import pygame


class Maze:
    def __init__(self, width, height, goal_position):
        self.width = width
        self.height = height
        self.cells = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.goal_position = goal_position
        self.goal_radius = min(width // len(self.cells[0]), height // len(self.cells)) // 6

    def draw(self, screen):
        gray = (169, 169, 169)
        white = (255, 255, 255)
        cell_width = self.width // len(self.cells[0])
        cell_height = self.height // len(self.cells)

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, gray, (x * cell_width, y * cell_height, cell_width, cell_height))
                else:
                    pygame.draw.rect(screen, white, (x * cell_width, y * cell_height, cell_width, cell_height))

        green = (0, 255, 0)
        pygame.draw.circle(
            screen,
            green,
            ((self.goal_position[1] + 1) * cell_width - cell_width // 2,
             self.goal_position[0] * cell_height + cell_height // 2),self.goal_radius
        )
