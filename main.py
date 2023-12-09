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

        self.goal_position = (6, 7)
        # Create the maze and agent
        self.maze = Maze(self.WIDTH, self.HEIGHT, self.goal_position)
        cell_width = self.WIDTH // len(self.maze.cells[0])
        cell_height = self.HEIGHT // len(self.maze.cells)
        self.agent = Agent((1, 1), self.goal_position, cell_width, cell_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.agent.move_up(self.maze)
                elif event.key == pygame.K_DOWN:
                    self.agent.move_down(self.maze)
                elif event.key == pygame.K_LEFT:
                    self.agent.move_left(self.maze)
                elif event.key == pygame.K_RIGHT:
                    self.agent.move_right(self.maze)
        return True

    def update_screen(self):
        self.screen.fill(self.BLACK)
        self.maze.draw(self.screen)
        cell_width = self.WIDTH // len(self.maze.cells[0])
        cell_height = self.HEIGHT // len(self.maze.cells)
        self.agent.draw(self.screen, cell_width, cell_height)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        time_passed = 0
        max_steps = 100
        while running:
            running = self.handle_events()
            dt = clock.tick(60)
            time_passed += dt
            while time_passed >= 100 and self.agent.is_alive and self.agent.steps_taken < max_steps:
                self.agent.think(self.maze)
                time_passed -= 100

            self.update_screen()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
