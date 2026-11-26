from pathlib import Path

import pygame


class ScrollingGround:
    def __init__(self, scroll_speed=120.0):
        self._scroll_offset = 0.0
        self._scroll_speed = scroll_speed
        image_path = (
                Path(__file__).resolve().parent
                / "assets" / "images" / "ground" / "ground_strip.png"
        )

        image = pygame.image.load(str(image_path)).convert_alpha()
        # Remove empty transparent space above the grass.
        image = image.subsurface(image.get_bounding_rect())

        self._height = 96
        # Preserve the artwork's proportions instead of stretching it.
        self._strip_width = round(image.get_width() * self._height / image.get_height())
        self._image = pygame.transform.smoothscale(
            image, (self._strip_width, self._height)
        )

    def update(self, dt: float):
        # Keep the offset between one strip left of the screen and zero.
        self._scroll_offset = -(
            (-self._scroll_offset + self._scroll_speed * dt) % self._strip_width
        )

    def draw(self, surface):
        ground_top = surface.get_height() - self._height

        # Include an extra strip to cover the right edge as the ground moves left.
        for x in range(0, surface.get_width() + self._strip_width, self._strip_width):
            surface.blit(self._image, (x + round(self._scroll_offset), ground_top))
