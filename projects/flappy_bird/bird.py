import pygame


class Bird:
    def __init__(self, position_x, position_y):
        self._width = 64
        self._height = 64
        self._position_x = position_x
        self._position_y = position_y
        self._collision_bound = pygame.Rect(position_x, position_y, self._width, self._height)
        # Positive velocity moves the bird down; negative velocity moves it up.
        # Hence, gravity is positive and flap velocity is negative.
        self._vertical_velocity = 0.0
        self._gravity = 1000.0
        self._flap_velocity = -350.0
        self._animation_frames = []
        self._current_frame_index = 0
        self._animation_timer = 0.0
        self._frame_duration = 0.04

    def flap(self):
        pass

    def update(self, dt: float):
        pass

    def draw(self, surface):
        pass
