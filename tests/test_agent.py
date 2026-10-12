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


if __name__ == "__main__": unittest.main()
