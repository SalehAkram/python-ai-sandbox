import pygame
from agents.agent import Agent
from mazes.maze import Maze


class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 640, 640
        self.BLACK = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simple Maze")

        # Create the maze and agent
        self.maze = Maze(self.WIDTH, self.HEIGHT)
        self.agent = Agent((1, 3), (6, 7))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.BLACK)
            self.maze.draw(self.screen)
            cell_width = self.WIDTH // len(self.maze.cells[0])
            cell_height = self.HEIGHT // len(self.maze.cells)
            self.agent.draw(self.screen, cell_width, cell_height)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
