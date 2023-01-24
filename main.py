import sys
from time import perf_counter_ns, perf_counter

import pygame
from pygame.locals import *

from Environment import Environment, GridSquareTerrain, GridSquareStructures

# ToDo: Use matplotlib to display the environment

def upon_exit():
    """
Function to be called upon wanting the pygame screen to close.
    """

    pygame.display.quit()
    sys.exit("Pygame screen close")


def main():
    # region - Initializing pygame
    pygame.init()
    pygame.display.set_caption("FPS: 000")
    window_size = (1280, 720)
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    # endregion - Initializing pygame

    # Environment
    everything_start = perf_counter()
    seed = 1

    start = perf_counter()
    env = Environment(100, 100)
    print("Generating Nodes:".ljust(30), perf_counter() - start, flush=True)

    start = perf_counter()
    env.generate_terrain(seed=seed)
    print("Generating Terrain:".ljust(30), perf_counter() - start, flush=True)

    env.set_player_base(1, 1)
    env.set_player_base(env.x_size - 3, env.y_size - 3)

    start = perf_counter()
    env.generate_natural_structures(tree_seed=seed, stone_seed=seed)
    print("Generating Natural Structures:".ljust(30), perf_counter() - start, flush=True)

    print("Whole Environment Setup:".ljust(30), perf_counter() - everything_start, flush=True)

    # region - Colours
    terrain_colours = {
        GridSquareTerrain.CLEAR: (70, 110, 45),
        GridSquareTerrain.HILL: (50, 80, 50),
        GridSquareTerrain.MOUNTAIN: (50, 55, 70),
        GridSquareTerrain.SNOW: (255, 255, 255)
    }

    structure_colours = {
        GridSquareStructures.PLAYER_BASE: (255, 0, 0),
        GridSquareStructures.TREE: (0, 255, 0),
        GridSquareStructures.STONE: (0, 0, 255)
    }
    # endregion

    # Environment map
    start = perf_counter()
    env_map = pygame.Surface((env.x_size, env.y_size))
    for x in range(env.x_size):
        for y in range(env.y_size):
            if env.grid[x, y].structure == GridSquareStructures.NONE:
                env_map.set_at((x, y), terrain_colours[env[x, y].terrain])
            else:
                env_map.set_at((x, y), structure_colours[env[x, y].structure])
    print("Creating Environment Map:".ljust(30), perf_counter() - start, flush=True)

    # Environment map scale and position
    scale = 7
    min_scale = 7
    max_scale = 48
    new_size = (round(env.x_size * scale), round(env.y_size * scale))
    position = [window_size[0] / 2 - env.x_size * scale / 2, window_size[1] / 2 - env.y_size * scale / 2]

    scaled_env_map = pygame.transform.scale(env_map, new_size)

    # Timings
    current_time = perf_counter_ns()
    old_time = current_time

    #
    old_size = (round(env.x_size * scale), round(env.y_size * scale))

    # Main loop
    while True:
        scale_changed = False
        for event in pygame.event.get():
            if event.type == QUIT:
                upon_exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    upon_exit()

                if event.key == K_SPACE:
                    print("Generating new terrain")
                    seed += 1
                    env = Environment(100, 100)
                    env.generate_terrain(seed=seed)
                    env.set_player_base(1, 1)
                    env.set_player_base(env.x_size - 3, env.y_size - 3)
                    env.generate_natural_structures(tree_seed=seed, stone_seed=seed)
                    for x in range(env.x_size):
                        for y in range(env.y_size):
                            if env.grid[x, y].structure == GridSquareStructures.NONE:
                                env_map.set_at((x, y), terrain_colours[env[x, y].terrain])
                            else:
                                env_map.set_at((x, y), structure_colours[env[x, y].structure])
                    scaled_env_map = pygame.transform.scale(env_map, new_size)

            if event.type == MOUSEWHEEL:
                scale_changed = True
                scale += event.y
                if scale < min_scale:
                    scale = min_scale
                elif scale > max_scale:
                    scale = max_scale

        screen.fill((0, 0, 0))

        """BELOW"""
        pressed = pygame.key.get_pressed()

        if pressed[K_a]:
            position[0] += 1 * scale
        if pressed[K_d]:
            position[0] -= 1 * scale
        if pressed[K_w]:
            position[1] += 1 * scale
        if pressed[K_s]:
            position[1] -= 1 * scale

        if scale_changed:
            position[0] -= (old_size[0] - new_size[0])
            position[1] -= (old_size[1] - new_size[1])
            new_size = (round(env.x_size * scale), round(env.y_size * scale))
            scaled_env_map = pygame.transform.scale(env_map, new_size)

        screen.blit(scaled_env_map, position)

        old_size = new_size
        """ABOVE"""

        pygame.display.flip()
        current_time = perf_counter_ns()
        fps = round(1_000_000_000 / (current_time - old_time))
        clock.tick(60)
        old_time = current_time
        pygame.display.set_caption(f"FPS: {fps}")


if __name__ == "__main__":
    main()
