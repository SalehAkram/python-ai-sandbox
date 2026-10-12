import unittest
from projects.maze_runner.evolution import EvolutionTrainer
from projects.maze_runner.maze import Maze


class EvolutionTests(unittest.TestCase):
    def test_generation_preserves_population_and_reports_stats(self):
        trainer = EvolutionTrainer(Maze(), population_size=12, max_steps=10, seed=7)
        stats, _ = trainer.run_generation(1)
        self.assertEqual(stats.generation, 1)
        self.assertEqual(len(trainer.population), 12)
        self.assertIsNotNone(trainer.best_brain)

    def test_training_is_reproducible(self):
        first = EvolutionTrainer(Maze(), population_size=10, max_steps=8, seed=3)
        second = EvolutionTrainer(Maze(), population_size=10, max_steps=8, seed=3)
        scores_a = [item.best_fitness for item in first.train(3)]
        scores_b = [item.best_fitness for item in second.train(3)]
        self.assertEqual(scores_a, scores_b)


if __name__ == "__main__": unittest.main()
