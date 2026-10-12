"""Maze-specific evaluation loop built on the shared genetic algorithm."""

from dataclasses import dataclass
import numpy as np
from projects.maze_runner.agent import Agent
from shared.neural_networks.neural_net import NeuralNetwork
from shared.neuroevolution.genetic_algorithm import breed_population


@dataclass(frozen=True)
class GenerationStats:
    generation: int
    best_fitness: float
    mean_fitness: float
    solved: int
    best_steps: int | None


class EvolutionTrainer:
    def __init__(self, maze, start=(1, 1), population_size=150, max_steps=80,
                 elite_fraction=0.1, mutation_rate=0.12, mutation_scale=0.25, seed=42):
        if population_size < 2:
            raise ValueError("population_size must be at least 2")
        self.maze, self.start = maze, start
        self.population_size, self.max_steps = population_size, max_steps
        self.elite_count = max(1, int(population_size * elite_fraction))
        self.mutation_rate, self.mutation_scale = mutation_rate, mutation_scale
        self.rng = np.random.default_rng(seed)
        self.distances = maze.distances_to_goal()
        if start not in self.distances:
            raise ValueError("the goal is not reachable from the start")
        self.population = [NeuralNetwork(8, 16, 4, self.rng)
                           for _ in range(population_size)]
        self.best_brain, self.best_fitness = None, float("-inf")

    def evaluate(self, brain):
        agent = Agent(self.start, self.maze.goal_position, self.maze.cell_width,
                      self.maze.cell_height, brain=brain)
        for _ in range(self.max_steps):
            if not agent.is_alive:
                break
            agent.think(self.maze)
        return agent, agent.fitness(self.distances, self.max_steps)

    def run_generation(self, generation):
        evaluated = [(brain, *self.evaluate(brain)) for brain in self.population]
        evaluated.sort(key=lambda item: item[2], reverse=True)
        best_brain, best_agent, best_score = evaluated[0]
        if best_score > self.best_fitness:
            self.best_fitness, self.best_brain = best_score, best_brain.clone()
        solved = [agent for _, agent, _ in evaluated if agent.reached_goal]
        stats = GenerationStats(generation, best_score,
                                float(np.mean([score for _, _, score in evaluated])),
                                len(solved), min((a.steps_taken for a in solved), default=None))
        self._breed(evaluated)
        return stats, best_agent

    def _breed(self, evaluated):
        ranked = [(brain, score) for brain, _agent, score in evaluated]
        self.population = breed_population(
            ranked, self.population_size, self.elite_count,
            self.mutation_rate, self.mutation_scale, self.rng,
        )

    def train(self, generations, callback=None, stop_when_solved=False):
        history = []
        for generation in range(1, generations + 1):
            stats, champion = self.run_generation(generation)
            history.append(stats)
            if callback:
                callback(stats, champion)
            if stop_when_solved and stats.solved:
                break
        return history
