"""Reusable selection, crossover, and mutation operations."""

import numpy as np


def breed_population(ranked, population_size, elite_count,
                     mutation_rate, mutation_scale, rng):
    """Create a new population from ``(genome, fitness)`` pairs, best first."""
    children = [genome.clone() for genome, _fitness in ranked[:elite_count]]
    pool = ranked[:max(2, population_size // 2)]
    weights = np.array([fitness for _genome, fitness in pool], dtype=float)
    weights /= weights.sum()

    while len(children) < population_size:
        first, second = rng.choice(len(pool), size=2, p=weights)
        child = pool[first][0].crossover(pool[second][0], rng)
        child.mutate(mutation_rate, mutation_scale, rng)
        children.append(child)
    return children
