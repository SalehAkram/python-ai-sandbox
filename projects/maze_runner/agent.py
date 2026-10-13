"""Maze Runner agent controlled by an evolvable neural network."""

import numpy as np
from shared.neural_networks.neural_net import NeuralNetwork

MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))


class Agent:
    def __init__(self, start, goal, cell_width=80, cell_height=80, brain=None, rng=None):
        self.position, self.start, self.goal = start, start, goal
        self.radius = min(cell_width, cell_height) // 6
        self.brain = brain or NeuralNetwork(8, 16, 4, rng=rng)
        self.steps_taken, self.invalid_moves = 0, 0
        self.reached_goal, self.is_alive = False, True
        self.path = [start]

    def cast_ray(self, maze, dx, dy):
        row, col = self.position
        max_distance = max(len(maze.cells), len(maze.cells[0]))
        for distance in range(max_distance):
            row, col = row + dy, col + dx
            if not maze.is_open((row, col)):
                return distance
        return max_distance

    def neural_inputs(self, maze):
        rows, cols = len(maze.cells), len(maze.cells[0])
        row, col = self.position
        goal_row, goal_col = self.goal
        scale = max(rows, cols)
        return np.array([self.cast_ray(maze, -1, 0) / scale,
                         self.cast_ray(maze, 1, 0) / scale,
                         self.cast_ray(maze, 0, -1) / scale,
                         self.cast_ray(maze, 0, 1) / scale,
                         (goal_col - col) / cols, (goal_row - row) / rows,
                         col / cols, row / rows])

    def think(self, maze):
        action = int(np.argmax(self.brain.feedforward(self.neural_inputs(maze))))
        self.move(maze, MOVES[action])
        return action

    def move(self, maze, delta):
        if not self.is_alive:
            return
        row, col = self.position
        candidate = (row + delta[0], col + delta[1])
        self.steps_taken += 1
        if maze.is_open(candidate):
            self.position = candidate
            self.path.append(candidate)
            self.reached_goal = candidate == self.goal
            if self.reached_goal:
                self.is_alive = False
        else:
            self.invalid_moves += 1

    def move_up(self, maze): self.move(maze, MOVES[0])
    def move_down(self, maze): self.move(maze, MOVES[1])
    def move_left(self, maze): self.move(maze, MOVES[2])
    def move_right(self, maze): self.move(maze, MOVES[3])

    def fitness(self, distances, max_steps):
        unique_cells = len(set(self.path))
        repeated_visits = len(self.path) - unique_cells
        best_distance = min(
            distances.get(position, max(distances.values()) + 1)
            for position in self.path
        )
        progress = distances[self.start] - best_distance
        score = (progress * 15.0 + unique_cells * 2.0
                 - self.invalid_moves * 0.5 - repeated_visits * 0.5)
        if self.reached_goal:
            score += 1_000 + (max_steps - self.steps_taken) * 5
        return max(0.01, score)

    def draw(self, screen, cell_width, cell_height, color=(255, 112, 72)):
        import pygame

        def cell_center(position):
            path_row, path_col = position
            return (path_col * cell_width + cell_width // 2,
                    path_row * cell_height + cell_height // 2)

        row, col = self.position
        center = cell_center((row, col))

        # A translucent overlay lets the trail and glow fade into the maze floor.
        effects = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        recent_path = self.path[-10:]
        for index in range(1, len(recent_path)):
            alpha = int(30 + 100 * index / len(recent_path))
            pygame.draw.line(
                effects,
                (*color, alpha),
                cell_center(recent_path[index - 1]),
                cell_center(recent_path[index]),
                width=max(2, self.radius // 3),
            )

        pygame.draw.circle(effects, (*color, 28), center, self.radius * 2)
        pygame.draw.circle(effects, (*color, 55), center, self.radius + 6)
        screen.blit(effects, (0, 0))

        # Dark shell, illuminated ring and central processor core.
        pygame.draw.circle(screen, (8, 16, 28), center, self.radius + 2)
        pygame.draw.circle(screen, color, center, self.radius, width=3)
        pygame.draw.circle(screen, (255, 205, 120), center,
                           max(4, self.radius // 2))
        pygame.draw.circle(screen, (255, 250, 220), center,
                           max(2, self.radius // 5))

        # Point toward the most recent successful movement direction.
        if len(self.path) > 1:
            previous_row, previous_col = self.path[-2]
            direction = (col - previous_col, row - previous_row)
            indicator_end = (
                center[0] + direction[0] * (self.radius + 7),
                center[1] + direction[1] * (self.radius + 7),
            )
            pygame.draw.line(screen, (255, 245, 205), center,
                             indicator_end, width=3)
            pygame.draw.circle(screen, color, indicator_end, 3)
