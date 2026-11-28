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
        self._heading_font = pygame.font.Font(None, 72)
        self._instruction_font = pygame.font.Font(None, 32)

        self._running = False
        self._state = GameState.Playing
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
                if self._state == GameState.Playing:
                    self._bird.flap()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self._state == GameState.Game_Over:
                    self.restart()

    def update(self, delta_time: float):
        if self._state != GameState.Playing:
            return
        self._bird.update(delta_time)
        self._ground.update(delta_time)
        self.collision_check()

    def collision_check(self):
        if self.collision_bird_ground():
            ground_top = self._screen.get_height() - self._ground.grounds_height
            self._bird.die(ground_top)
            self._state = GameState.Game_Over

    def collision_bird_ground(self):
        return self._bird.birds_bottom >= self._screen.get_height() - self._ground.grounds_height

    def render(self):
        self._screen.fill((135, 206, 235))
        self._bird.draw(self._screen)
        self._ground.draw(self._screen)
        if self._state == GameState.Game_Over:
            overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))
            self._screen.blit(overlay, (0, 0))
            center_x, center_y = self._screen.get_rect().center
            heading = self._heading_font.render("Game Over", True, (255, 255, 255))
            instruction = self._instruction_font.render(
                "Press R to restart", True, (255, 255, 255)
            )
            self._screen.blit(heading, heading.get_rect(center=(center_x, center_y - 30)))
            self._screen.blit(instruction, instruction.get_rect(center=(center_x, center_y + 30)))
        pygame.display.flip()

    def restart(self):
        self._bird.reset()
        self._ground.reset()
        self._pipe_pairs.clear()
        self._score = 0
        self._state = GameState.Playing
