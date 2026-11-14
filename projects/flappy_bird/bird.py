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
        self._vertical_velocity = self._flap_velocity

    def update(self, dt: float):
        self._move_bird(dt)
        self._animation_timer += dt

        while self._animation_timer >= self._frame_duration:
            self._animation_timer -= self._frame_duration
            self._current_frame_index = (self._current_frame_index + 1) % len(self._animation_frames)

    def _move_bird(self, dt: float):
        self._vertical_velocity += self._gravity * dt
        self._position_y += self._vertical_velocity * dt
        self._collision_bound = pygame.Rect(self._position_x, self._position_y, self._width, self._height)

    def draw(self, surface):
        current_frame = self._animation_frames[self._current_frame_index]
        surface.blit(current_frame, (self._position_x, self._position_y))
