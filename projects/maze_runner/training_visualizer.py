"""Live Pygame presentation of a population evolving through a maze."""

import copy
import math
from projects.maze_runner.agent import MOVES


class TrainingVisualizer:
    PANEL_WIDTH = 280

    def __init__(self, maze, fps=60, generation_interval=10, max_steps=80):
        import pygame

        pygame.init()
        self.pygame = pygame
        self.maze = maze
        self.screen = pygame.display.set_mode(
            (maze.width + self.PANEL_WIDTH, maze.height)
        )
        pygame.display.set_caption("Maze Runner - Evolution Lab")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.generation_interval = generation_interval
        self.max_steps = max_steps
        self.distances = maze.distances_to_goal()
        self.best_ever_fitness = None
        self.active = True
        self.heading_font = pygame.font.Font(None, 34)
        self.label_font = pygame.font.Font(None, 24)
        self.value_font = pygame.font.Font(None, 30)

    def update_population(self, generation, step, agents):
        if not self.active:
            return
        if generation != 1 and generation % self.generation_interval != 0:
            self._handle_events()
            return

        self._handle_events()
        if not self.active:
            return

        self.maze.draw(self.screen)
        self._draw_population(agents)
        self._draw_live_panel(generation, step, agents)
        self.pygame.display.flip()
        self.clock.tick(self.fps)

    def record_stats(self, stats):
        if (self.best_ever_fitness is None
                or stats.best_fitness > self.best_ever_fitness):
            self.best_ever_fitness = stats.best_fitness

    def update_summary(self, stats, agent):
        if not self.active:
            return
        self._handle_events()
        if not self.active:
            return

        self.maze.draw(self.screen)
        agent.draw(self.screen, self.maze.cell_width, self.maze.cell_height)
        self._draw_summary_panel(stats, agent)
        self.pygame.display.flip()

        if stats.solved:
            self._replay_solution(stats, agent)

    def _draw_population(self, agents):
        overlay = self.pygame.Surface(self.screen.get_size(), self.pygame.SRCALPHA)
        cell_width = self.maze.cell_width
        cell_height = self.maze.cell_height

        for index, agent in enumerate(agents):
            row, col = agent.position
            angle = index * 2.399963
            radius = 2 + (index % 5) * 1.4
            center = (
                int(col * cell_width + cell_width / 2 + math.cos(angle) * radius),
                int(row * cell_height + cell_height / 2 + math.sin(angle) * radius),
            )
            agent_color = ((55, 220, 140, 150) if agent.reached_goal
                           else (255, 112, 72, 75))

            if agent.last_action is not None and not agent.last_move_valid:
                move_row, move_col = MOVES[agent.last_action]
                collision_end = (
                    center[0] + move_col * int(cell_width * 0.3),
                    center[1] + move_row * int(cell_height * 0.3),
                )
                self.pygame.draw.line(
                    overlay, (255, 70, 85, 120), center, collision_end, width=2
                )
                self.pygame.draw.circle(
                    overlay, (255, 170, 120, 170), collision_end, 2
                )

            if len(agent.path) > 1:
                previous_row, previous_col = agent.path[-2]
                previous = (
                    previous_col * cell_width + cell_width // 2,
                    previous_row * cell_height + cell_height // 2,
                )
                self.pygame.draw.line(overlay, (*agent_color[:3], 25),
                                      previous, center, width=1)
            self.pygame.draw.circle(overlay, agent_color, center, 3)

        self.screen.blit(overlay, (0, 0))

    def _draw_live_panel(self, generation, step, agents):
        active = sum(agent.is_alive for agent in agents)
        solved = sum(agent.reached_goal for agent in agents)
        collisions = sum(agent.last_move_valid is False for agent in agents)
        live_best = max(
            agent.fitness(self.distances, self.max_steps) for agent in agents
        )
        best_ever = (f"{self.best_ever_fitness:.1f}"
                     if self.best_ever_fitness is not None else "--")
        rows = (
            ("GENERATION", generation),
            ("EVALUATION STEP", step),
            ("ACTIVE AGENTS", active),
            ("GOAL REACHED", solved),
            ("WALL COLLISIONS", collisions),
            ("LIVE BEST FITNESS", f"{live_best:.1f}"),
            ("BEST EVER FITNESS", best_ever),
        )
        self._draw_panel_base("SWARM EVALUATION", "POPULATION IN MOTION")
        self._draw_rows(rows)
        status = "SOLUTION FOUND" if solved else "EVALUATING"
        status_color = (55, 220, 140) if solved else (255, 112, 72)
        self._draw_status(status, status_color)

    def _draw_summary_panel(self, stats, agent):
        self._draw_panel_base("EVOLUTION LAB", "BEST AGENT THIS GENERATION")
        best_steps = stats.best_steps if stats.best_steps is not None else "--"
        rows = (
            ("GENERATION", stats.generation),
            ("BEST FITNESS", f"{stats.best_fitness:.1f}"),
            ("MEAN FITNESS", f"{stats.mean_fitness:.1f}"),
            ("SOLVED", stats.solved),
            ("BEST STEPS", best_steps),
            ("UNIQUE CELLS", len(set(agent.path))),
        )
        self._draw_rows(rows)
        status = "GOAL REACHED" if stats.solved else "EVOLVING"
        status_color = (55, 220, 140) if stats.solved else (255, 112, 72)
        self._draw_status(status, status_color)

    def _draw_panel_base(self, heading, subtitle):
        panel_left = self.maze.width
        panel = self.pygame.Rect(
            panel_left, 0, self.PANEL_WIDTH, self.maze.height
        )
        self.pygame.draw.rect(self.screen, (8, 16, 28), panel)
        self.pygame.draw.line(
            self.screen,
            (36, 180, 200),
            (panel_left, 0),
            (panel_left, self.maze.height),
            width=2,
        )

        self._text(heading, self.heading_font,
                   (90, 225, 240), panel_left + 24, 30)
        self._text(subtitle, self.label_font,
                   (130, 155, 170), panel_left + 24, 72)

    def _draw_rows(self, rows):
        panel_left = self.maze.width
        y = 122
        for label, value in rows:
            self._text(label, self.label_font, (110, 140, 155),
                       panel_left + 24, y)
            self._text(str(value), self.value_font, (245, 245, 225),
                       panel_left + 24, y + 24)
            y += 64

    def _draw_status(self, status, status_color):
        panel_left = self.maze.width
        self._text(status, self.value_font, status_color,
                   panel_left + 24, self.maze.height - 64)

    def _replay_solution(self, stats, agent):
        replay_agent = copy.copy(agent)
        complete_path = list(agent.path)
        for path_end in range(1, len(complete_path) + 1):
            self._handle_events()
            if not self.active:
                return
            replay_agent.path = complete_path[:path_end]
            replay_agent.position = replay_agent.path[-1]
            self.maze.draw(self.screen)
            replay_agent.draw(
                self.screen, self.maze.cell_width, self.maze.cell_height
            )
            self._draw_summary_panel(stats, replay_agent)
            self.pygame.display.flip()
            self.clock.tick(min(self.fps, 12))

    def _handle_events(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.active = False

    def _text(self, text, font, color, x, y):
        surface = font.render(str(text), True, color)
        self.screen.blit(surface, (x, y))

    def close(self):
        self.pygame.quit()
