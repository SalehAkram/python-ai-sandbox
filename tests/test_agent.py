import unittest
import numpy as np
from projects.maze_runner.agent import Agent
from projects.maze_runner.maze import Maze


class FixedBrain:
    def __init__(self, action): self.action = action
    def feedforward(self, _inputs):
        output = np.zeros((4, 1)); output[self.action] = 1
        return output


class AgentTests(unittest.TestCase):
    def setUp(self): self.maze = Maze()

    def test_rays_measure_open_cells_before_a_wall(self):
        agent = Agent((1, 1), self.maze.goal_position)
        self.assertEqual(agent.cast_ray(self.maze, -1, 0), 0)
        self.assertEqual(agent.cast_ray(self.maze, 1, 0), 5)

    def test_valid_move_updates_position(self):
        agent = Agent((1, 1), self.maze.goal_position, brain=FixedBrain(3))
        agent.think(self.maze)
        self.assertEqual(agent.position, (1, 2))
        self.assertEqual(agent.steps_taken, 1)

    def test_wall_collision_is_penalized_without_killing_agent(self):
        agent = Agent((1, 1), self.maze.goal_position, brain=FixedBrain(0))
        agent.think(self.maze)
        self.assertEqual(agent.position, (1, 1))
        self.assertEqual(agent.invalid_moves, 1)
        self.assertTrue(agent.is_alive)

    def test_fitness_remembers_best_progress(self):
        agent = Agent((1, 1), self.maze.goal_position)
        agent.path = [(1, 1), (2, 1), (3, 1), (2, 1), (1, 1)]
        agent.position = (1, 1)

        score = agent.fitness(self.maze.distances_to_goal(), max_steps=80)

        self.assertGreater(score, 30.0)

    def test_fitness_penalizes_repeated_visits(self):
        direct = Agent((1, 1), self.maze.goal_position)
        direct.path = [(1, 1), (1, 2), (1, 3)]
        direct.position = (1, 3)

        looping = Agent((1, 1), self.maze.goal_position)
        looping.path = [(1, 1), (1, 2), (1, 3), (1, 2), (1, 3)]
        looping.position = (1, 3)

        distances = self.maze.distances_to_goal()
        self.assertLess(
            looping.fitness(distances, max_steps=80),
            direct.fitness(distances, max_steps=80),
        )


if __name__ == "__main__": unittest.main()
