import sys
from time import perf_counter_ns

import pygame
from pygame.locals import *

from Environment import Environment, GridSquareTerrain, GridSquareStructures


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
    seed = 1
    env = Environment(100, 100)
    env.generate_terrain(seed=seed)

    env.set_player_base(1, 1)
    env.set_player_base(env.x_size - 3, env.y_size - 3)

    env.generate_natural_structures(seed=seed)

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
    env_map = pygame.Surface((env.x_size, env.y_size))
    for x in range(env.x_size):
        for y in range(env.y_size):
            if env.grid[x, y].structure == GridSquareStructures.NONE:
                env_map.set_at((x, y), terrain_colours[env[x, y].terrain])
            else:
                env_map.set_at((x, y), structure_colours[env[x, y].structure])

    # Environment map scale and position
    scale = 3
    position = [window_size[0] / 2 - env.x_size * scale / 2, window_size[1] / 2 - env.y_size * scale / 2]

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

            if event.type == MOUSEWHEEL:
                scale_changed = True
                scale += event.y / 10

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

        new_size = (round(env.x_size * scale), round(env.y_size * scale))

        if scale_changed:
            position[0] += (old_size[0] - new_size[0]) / 2
            position[1] += (old_size[1] - new_size[1]) / 2

        screen.blit(pygame.transform.scale(env_map, new_size), position)

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
