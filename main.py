import os
import time

import numpy as np
import pygame

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_ALIVE = (255, 255, 255)
COLOR_ALIVE_NEXT = (107, 161, 74)
COLOR_DIE_NEXT = (171, 44, 44)
CELL_SIZE = 20
ROWS = 30
COLUMNS = 40
SEED_FILENAME = "seed.txt"


def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    return updated_cells


def setup_cells():
    return np.loadtxt(SEED_FILENAME, dtype=int) if os.path.isfile(SEED_FILENAME) else np.zeros((ROWS, COLUMNS))


def save_state(cells):
    np.savetxt(SEED_FILENAME, cells, fmt='%d')


def main():
    pygame.init()
    screen = pygame.display.set_mode((COLUMNS * CELL_SIZE, ROWS * CELL_SIZE))

    cells = setup_cells()
    screen.fill(COLOR_GRID)
    update(screen, cells, CELL_SIZE)

    pygame.display.flip()
    pygame.display.update()

    running = False
    automatic = False
    next_move = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    print("Running", running)
                    update(screen, cells, CELL_SIZE)
                    pygame.display.update()
                if event.key == pygame.K_a:
                    automatic = not automatic
                    print("Automatic", automatic)
                if event.key == pygame.K_s:
                    print("Save cells")
                    save_state(cells)
                if event.key == pygame.K_r:
                    print("Reset cells")
                    cells = setup_cells()
                    update(screen, cells, CELL_SIZE)
                    pygame.display.update()
                if event.key == pygame.K_RIGHT:
                    print("Next state")
                    next_move = True
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                cells[x, y] = not cells[x, y]
                update(screen, cells, CELL_SIZE)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running and (automatic or next_move):
            next_move = False
            cells = update(screen, cells, CELL_SIZE, with_progress=False)
            pygame.display.update()
            time.sleep(0.15)
        else:
            time.sleep(0.001)




if __name__ == '__main__':
    main()
