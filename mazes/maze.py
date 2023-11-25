import pygame


class Maze:
    def __init__(self, width, height):
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

    def draw(self, screen):
        GRAY = (169, 169, 169)
        WHITE = (255, 255, 255)
        cell_width = self.width // len(self.cells[0])
        cell_height = self.height // len(self.cells)

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, GRAY, (x * cell_width, y * cell_height, cell_width, cell_height))
                else:
                    pygame.draw.rect(screen, WHITE, (x * cell_width, y * cell_height, cell_width, cell_height))
