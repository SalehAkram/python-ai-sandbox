"""Command-line entry point for training and replaying Maze Runner agents."""

import argparse
from pathlib import Path
from projects.maze_runner.agent import Agent
from projects.maze_runner.evolution import EvolutionTrainer
from projects.maze_runner.maze import Maze
from shared.neural_networks.neural_net import NeuralNetwork


def replay(brain, maze=None, max_steps=80):
    import pygame
    maze = maze or Maze()
    agent = Agent((1, 1), maze.goal_position, maze.cell_width, maze.cell_height, brain=brain)
    pygame.init()
    screen = pygame.display.set_mode((maze.width, maze.height))
    pygame.display.set_caption("Maze Runner - Neuroevolution")
    clock, running = pygame.time.Clock(), True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if agent.is_alive and agent.steps_taken < max_steps:
            agent.think(maze)
        maze.draw(screen)
        agent.draw(screen, maze.cell_width, maze.cell_height)
        pygame.display.flip()
        clock.tick(8)
    pygame.quit()


def train(args):
    maze = Maze()
    trainer = EvolutionTrainer(maze, population_size=args.population,
                               max_steps=args.steps, seed=args.seed)
    visualizer = None
    if args.show_training:
        from projects.maze_runner.training_visualizer import TrainingVisualizer
        visualizer = TrainingVisualizer(
            maze, args.training_fps, args.training_interval, args.steps
        )

    def report(stats, champion):
        if stats.generation == 1 or stats.generation % args.log_every == 0 or stats.solved:
            steps = stats.best_steps if stats.best_steps is not None else "-"
            print(f"generation={stats.generation:4d} best={stats.best_fitness:7.2f} "
                  f"mean={stats.mean_fitness:7.2f} solved={stats.solved:3d} steps={steps}")
        if visualizer:
            visualizer.record_stats(stats)
            if stats.solved:
                visualizer.update_summary(stats, champion)

    step_callback = visualizer.update_population if visualizer else None
    history = trainer.train(
        args.generations,
        report,
        args.stop_when_solved,
        step_callback=step_callback,
    )
    if visualizer:
        visualizer.close()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    trainer.best_brain.save(output)
    print(f"Saved champion to {output} after {len(history)} generations.")
    if args.visualize:
        replay(trainer.best_brain, maze, args.steps)


def parse_args():
    parser = argparse.ArgumentParser(description="Evolve a neural network to solve a maze.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    training = subparsers.add_parser("train", help="run headless neuroevolution")
    training.add_argument("--generations", type=int, default=200)
    training.add_argument("--population", type=int, default=150)
    training.add_argument("--steps", type=int, default=80)
    training.add_argument("--seed", type=int, default=42)
    training.add_argument("--log-every", type=int, default=10)
    training.add_argument("--output", default="artifacts/maze_runner/champion.npz")
    training.add_argument("--stop-when-solved", action="store_true")
    training.add_argument("--show-training", action="store_true",
                          help="animate the population in sampled generations")
    training.add_argument("--training-fps", type=int, default=60,
                          help="population animation frames per second")
    training.add_argument("--training-interval", type=int, default=10,
                          help="animate every Nth generation (plus generation 1)")
    training.add_argument("--visualize", action="store_true")
    replay_parser = subparsers.add_parser("replay", help="visualize a saved champion")
    replay_parser.add_argument("model", nargs="?", default="artifacts/maze_runner/champion.npz")
    replay_parser.add_argument("--steps", type=int, default=80)
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "train":
        train(args)
    else:
        replay(NeuralNetwork.load(args.model), max_steps=args.steps)


if __name__ == "__main__":
    main()
