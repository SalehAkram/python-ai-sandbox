import pygame

from pathlib import Path


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
        # load the bird frames
        self._animation_frames = []
        self._load_animation_frames()

        self._current_frame_index = 0
        self._animation_timer = 0.0
        self._frame_duration = 0.04

    def _load_animation_frames(self):
        bird_folder = Path(__file__).resolve().parent
        frames_folder = bird_folder / "assets" / "images" / "bird"

        frame_paths = sorted(frames_folder.glob("*.png"))

        for frame_path in frame_paths:
            image = pygame.image.load(str(frame_path)).convert_alpha()
            scaled_image = pygame.transform.smoothscale(
                image,
                (self._width, self._height),
            )
            self._animation_frames.append(scaled_image)

    def flap(self):
        pass

    def update(self, dt: float):
        pass

    def draw(self, surface):
        current_frame = self._animation_frames[self._current_frame_index]
        surface.blit(current_frame, (self._position_x, self._position_y))
