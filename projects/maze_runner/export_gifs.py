"""Export portfolio-ready Maze Runner GIFs from a deterministic training run."""

import argparse
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from PIL import Image

from projects.maze_runner.agent import Agent
from projects.maze_runner.evolution import EvolutionTrainer
from projects.maze_runner.maze import Maze
from projects.maze_runner.training_visualizer import TrainingVisualizer


MILESTONE_GENERATIONS = (1, 10, 25, 50, 75)
CAPTURE_STEPS = frozenset((*range(0, 21), 30, 50, 80))


def screen_image(pygame, screen):
    """Copy the current Pygame surface into a Pillow image."""
    size = screen.get_size()
    pixels = pygame.image.tobytes(screen, "RGB")
    return Image.frombytes("RGB", size, pixels)


def save_gif(frames, path, duration=85):
    """Save frames with a compact shared-size adaptive colour palette."""
    path.parent.mkdir(parents=True, exist_ok=True)
    quantized = [
        frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
        for frame in frames
    ]
    quantized[0].save(
        path,
        save_all=True,
        append_images=quantized[1:],
        duration=duration,
        loop=0,
        optimize=True,
        disposal=2,
    )


def discover_solved_generation(maze, generations, population, steps, seed):
    trainer = EvolutionTrainer(
        maze,
        population_size=population,
        max_steps=steps,
        seed=seed,
    )
    history = trainer.train(generations, stop_when_solved=True)
    if not history[-1].solved:
        raise RuntimeError(f"No solution evolved within {generations} generations")
    return history[-1].generation


def export(output_dir, generations=300, population=150, steps=80, seed=42):
    maze = Maze()
    solved_generation = discover_solved_generation(
        maze, generations, population, steps, seed
    )
    milestones = set(MILESTONE_GENERATIONS) | {solved_generation}

    trainer = EvolutionTrainer(
        maze,
        population_size=population,
        max_steps=steps,
        seed=seed,
    )
    visualizer = TrainingVisualizer(
        maze,
        fps=1000,
        generation_interval=1,
        max_steps=steps,
    )
    training_frames = []
    final_stats = None

    def capture_step(generation, step, agents):
        if generation not in milestones or step not in CAPTURE_STEPS:
            return
        visualizer.update_population(generation, step, agents)
        frame = screen_image(visualizer.pygame, visualizer.screen)
        training_frames.append(frame)
        if step == 0:
            training_frames.extend([frame.copy()] * 3)

    for generation in range(1, generations + 1):
        stats, _champion = trainer.run_generation(generation, capture_step)
        visualizer.record_stats(stats)
        final_stats = stats
        if stats.solved:
            break

    if final_stats is None or not final_stats.solved:
        visualizer.close()
        raise RuntimeError("Captured training run did not reproduce its solution")

    output_dir = Path(output_dir)
    training_path = output_dir / "maze-runner-evolution.gif"
    save_gif(training_frames, training_path)

    champion = Agent(
        (1, 1), maze.goal_position, maze.cell_width, maze.cell_height,
        brain=trainer.best_brain,
    )
    champion_frames = []

    def capture_champion_frame():
        maze.draw(visualizer.screen)
        champion.draw(
            visualizer.screen, maze.cell_width, maze.cell_height
        )
        full_frame = screen_image(visualizer.pygame, visualizer.screen)
        champion_frames.append(full_frame.crop((0, 0, maze.width, maze.height)))

    capture_champion_frame()
    champion_frames.extend([champion_frames[-1].copy()] * 3)
    while champion.is_alive and champion.steps_taken < steps:
        champion.think(maze)
        capture_champion_frame()
    champion_frames.extend([champion_frames[-1].copy()] * 8)

    champion_path = output_dir / "maze-runner-champion.gif"
    save_gif(champion_frames, champion_path, duration=180)
    visualizer.close()

    return training_path, champion_path, solved_generation, champion.steps_taken


def parse_args():
    parser = argparse.ArgumentParser(description="Export Maze Runner portfolio GIFs.")
    parser.add_argument("--output-dir", default="docs/assets/maze_runner")
    parser.add_argument("--generations", type=int, default=300)
    parser.add_argument("--population", type=int, default=150)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main():
    args = parse_args()
    result = export(
        args.output_dir,
        args.generations,
        args.population,
        args.steps,
        args.seed,
    )
    training_path, champion_path, solved_generation, champion_steps = result
    print(f"Evolution GIF: {training_path}")
    print(f"Champion GIF: {champion_path}")
    print(f"Solved at generation {solved_generation} in {champion_steps} steps")


if __name__ == "__main__":
    main()
