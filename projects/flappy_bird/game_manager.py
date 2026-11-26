from enum import Enum
import pygame
from typing import List
from projects.flappy_bird.bird import Bird
from projects.flappy_bird.pipe_pair import PipePair
from projects.flappy_bird.scrolling_ground import ScrollingGround


class GameState(Enum):
    Ready = 1
    Playing = 2
    Game_Over = 3


class GameManager:
    def __init__(self):
        # Initialise Pygame before creating the display and game objects.
        pygame.init()
        self._screen = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Flappy Bird")
        self._clock = pygame.time.Clock()

        self._running = False
        self._state = GameState.Ready
        self._score = 0

        self._bird = Bird(100, 280)
        self._pipe_pairs: List[PipePair] = []
        self._ground = ScrollingGround(scroll_speed=120.0)

    def run(self):
        self._running = True

        try:
            while self._running:
                delta_time = self._clock.tick(60) / 1000.0

                self.handle_events()
                if not self._running:
                    break

                self.update(delta_time)
                self.render()
        finally:
            pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._bird.flap()

    def update(self, delta_time: float):
        self._bird.update(delta_time)
        self._ground.update(delta_time)

    def render(self):
        self._screen.fill((135, 206, 235))
        self._bird.draw(self._screen)
        self._ground.draw(self._screen)
        pygame.display.flip()

    def restart(self):
        pass
