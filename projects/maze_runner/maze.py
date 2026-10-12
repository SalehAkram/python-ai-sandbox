"""Maze Runner environment and optional Pygame renderer."""

from collections import deque


LAB_BACKGROUND = (7, 12, 24)
FLOOR_COLOR = (12, 22, 38)
GRID_COLOR = (23, 47, 66)

WALL_EDGE_COLOR = (36, 180, 200)
WALL_COLOR = (18, 54, 72)
WALL_INNER_COLOR = (14, 39, 55)

GOAL_GLOW_COLOR = (20, 75, 58)
GOAL_RING_COLOR = (55, 220, 140)
GOAL_CORE_COLOR = (170, 255, 210)


DEFAULT_CELLS = (
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 1, 1, 1, 1, 0, 1),
    (1, 0, 1, 0, 0, 0, 0, 1),
    (1, 0, 1, 0, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1),
)


class Maze:
    def __init__(self, width=640, height=640, goal_position=(6, 7), cells=DEFAULT_CELLS):
        self.width, self.height = width, height
        self.cells = [list(row) for row in cells]
        self.goal_position = goal_position
        self.goal_radius = min(self.cell_width, self.cell_height) // 6

    @property
    def cell_width(self): return self.width // len(self.cells[0])

    @property
    def cell_height(self): return self.height // len(self.cells)

    def is_open(self, position):
        row, col = position
        return (0 <= row < len(self.cells) and 0 <= col < len(self.cells[0])
                and self.cells[row][col] == 0)

    def distances_to_goal(self):
        distances = {self.goal_position: 0}
        queue = deque([self.goal_position])
        while queue:
            row, col = queue.popleft()
            for candidate in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                if self.is_open(candidate) and candidate not in distances:
                    distances[candidate] = distances[(row, col)] + 1
                    queue.append(candidate)
        return distances

    def draw(self, screen):
        import pygame

        screen.fill(LAB_BACKGROUND)

        for row_index, row in enumerate(self.cells):
            for column_index, cell in enumerate(row):
                cell_rect = pygame.Rect(
                    column_index * self.cell_width,
                    row_index * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )

                if cell == 1:
                    pygame.draw.rect(screen, WALL_EDGE_COLOR, cell_rect)

                    inner_wall = cell_rect.inflate(-6, -6)
                    pygame.draw.rect(
                        screen,
                        WALL_COLOR,
                        inner_wall,
                        border_radius=5,
                    )

                    inner_panel = inner_wall.inflate(-8, -8)
                    pygame.draw.rect(
                        screen,
                        WALL_INNER_COLOR,
                        inner_panel,
                        border_radius=3,
                    )
                else:
                    pygame.draw.rect(screen, FLOOR_COLOR, cell_rect)
                    pygame.draw.rect(screen, GRID_COLOR, cell_rect, width=1)

        self._draw_goal(screen)

    def _draw_goal(self, screen):
        import pygame

        row, col = self.goal_position
        center = (col * self.cell_width + self.cell_width // 2,
                  row * self.cell_height + self.cell_height // 2)
        outer_radius = self.goal_radius * 2

        pygame.draw.circle(screen, GOAL_GLOW_COLOR, center, outer_radius)
        pygame.draw.circle(
            screen,
            GOAL_RING_COLOR,
            center,
            outer_radius,
            width=3,
        )
        pygame.draw.circle(
            screen,
            GOAL_RING_COLOR,
            center,
            self.goal_radius,
            width=2,
        )
        pygame.draw.circle(
            screen,
            GOAL_CORE_COLOR,
            center,
            max(3, self.goal_radius // 3),
        )

        crosshair_start = outer_radius + 4
        crosshair_end = outer_radius + 10
        center_x, center_y = center
        crosshairs = (
            ((center_x - crosshair_end, center_y),
             (center_x - crosshair_start, center_y)),
            ((center_x + crosshair_start, center_y),
             (center_x + crosshair_end, center_y)),
            ((center_x, center_y - crosshair_end),
             (center_x, center_y - crosshair_start)),
            ((center_x, center_y + crosshair_start),
             (center_x, center_y + crosshair_end)),
        )
        for start, end in crosshairs:
            pygame.draw.line(screen, GOAL_RING_COLOR, start, end, width=2)
