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
        distance = distances.get(self.position, max(distances.values()) + 1)
        progress = distances[self.start] - distance
        score = progress * 15.0 + len(set(self.path)) * 2.0 - self.invalid_moves * 0.5
        if self.reached_goal:
            score += 1_000 + (max_steps - self.steps_taken) * 5
        return max(0.01, score)

    def draw(self, screen, cell_width, cell_height, color=(255, 85, 85)):
        import pygame
        row, col = self.position
        center = (col * cell_width + cell_width // 2, row * cell_height + cell_height // 2)
        pygame.draw.circle(screen, color, center, self.radius)
