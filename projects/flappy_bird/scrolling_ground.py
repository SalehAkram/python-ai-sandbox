from pathlib import Path

import pygame


class ScrollingGround:
    def __init__(self):
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

    def draw(self, surface):
        ground_top = surface.get_height() - self._height

        for x in range(0, surface.get_width(), self._strip_width):
            surface.blit(self._image, (x, ground_top))
