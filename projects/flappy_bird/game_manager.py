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
        self._screen = pygame.display.set_mode((480, 640))
        pygame.display.set_caption("Flappy Bird")
        self._clock = pygame.time.Clock()

        self._running = False
        self._state = GameState.Ready
        self._score = 0

        self._bird = Bird()
        self._pipe_pairs: List[PipePair] = []
        self._ground = ScrollingGround()

    def run(self):
        pass

    def handle_events(self):
        pass

    def update(self, delta_time: float):
        pass

    def render(self):
        pass

    def restart(self):
        pass
