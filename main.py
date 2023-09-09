from maze import Maze
import pygame


def lines(screen, WIDTH, HEIGHT, BLOCKSIZE):
    """
    Draws grid lines for rows and columns on the screen within the world.

    Runtime: O(n)

    Args:
        screen: Pygame screen object to draw on.
        WIDTH: Total width of the world.
        HEIGHT: Total height of the world.
        BLOCKSIZE: Size of each grid block in the world.
    """
    for line_row in range(0, WIDTH, BLOCKSIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, line_row), (WIDTH, line_row), width=1)
    for line_col in range(0, HEIGHT, BLOCKSIZE):
        pygame.draw.line(screen, (255, 255, 255), (line_col, 0), (line_col, HEIGHT), width=1)


def draw_world(screen, WORLD, WIDTH, HEIGHT, BLOCKSIZE):
    """
    Draws the current state of the matrix.

    The world model is represented as a matrix with dimensions (WIDTH // BLOCKSIZE) by (HEIGHT // BLOCKSIZE).
       
    Runtime: O(n**2)

    Args:
        screen: Pygame screen object to draw on.
        WIDTH: Total width of the world.
        HEIGHT: Total height of the world.
        BLOCKSIZE: Size of each grid block in the world.
        WORLD: The matrix.
    """
    for i in range(len(WORLD)):
        for j in range(len(WORLD[0])):
            x = j * BLOCKSIZE
            y = i * BLOCKSIZE

            if WORLD[i][j] == 1:
                pygame.draw.rect(screen, (127, 127, 127), pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE).move(x, y), width=0)

            if WORLD[i][j] == 0:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE).move(x, y), width=0)

            if WORLD[i][j] == "s":
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE).move(x, y), width=0)

            if WORLD[i][j] == "d":
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE).move(x, y), width=0)

            if WORLD[i][j] == "#":
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, BLOCKSIZE, BLOCKSIZE).move(x, y), width=0)


def game():
    """
    WIDTH, HEIGHT: Number of rows and columns in pixels.

    BLOCKSIZE: Size of each square in the world.
    You can change the BLOCKSIZE to create a larger or smaller world.

    In the matrix, each entry is represented as either a 1 or a 0. A 1 signifies a possible path,
    while a 0 indicates a wall.

    Runtime: O(n)

    Example Matrix:

    WORLD = [[1, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 1, 1]
            [0, 0, 1, 1]] 
    """
    WIDTH, HEIGHT = 1000, 1000
    BLOCKSIZE = 25
    WORLD = [[1 for i in range(WIDTH // BLOCKSIZE)] for j in range(HEIGHT // BLOCKSIZE)]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('pathfinder')
    running = True
    pressed = False
    operation = "SET_START"

    while running:
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                j = mouse_position[0] // BLOCKSIZE
                i = mouse_position[1] // BLOCKSIZE

                if event.button == 1 and operation == "SET_START":
                    if (WORLD[i][j] == 1):
                        WORLD[i][j] = "s"
                    start = j + i * (HEIGHT // BLOCKSIZE)
                    operation = "SET_DESTINATION"

                if event.button == 1 and WORLD[i][j] != "s" and operation == "SET_DESTINATION":
                    if (WORLD[i][j] == 1):
                        WORLD[i][j] = "d"
                    operation = "SET_OBSTACLE"
                    end = j + i * (HEIGHT // BLOCKSIZE)

                if event.button == 1 and (WORLD[i][j] != "s" or WORLD[i][j] != "d") and operation == "SET_OBSTACLE":
                    if (WORLD[i][j] == 1):
                        WORLD[i][j] = 0

                if event.button == 1 and (WORLD[i][j] != "s" or WORLD[i][j] != "d") and operation == "SET_OBSTACLE":
                    pressed = True

            if event.type == pygame.MOUSEBUTTONUP and operation == "SET_OBSTACLE":
                if event.button == 1 and operation == "SET_OBSTACLE":
                    pressed = False

            if pressed and operation == "SET_OBSTACLE":
                current_pos = pygame.mouse.get_pos()
                j = current_pos[0] // BLOCKSIZE
                i = current_pos[1] // BLOCKSIZE

                if WORLD[i][j] != "s" and WORLD[i][j] != "d":
                    WORLD[i][j] = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    maze = Maze(WORLD)
                    WORLD = maze.shortest_path(start, end)

                if event.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    game()

        draw_world(screen, WORLD, WIDTH, HEIGHT, BLOCKSIZE)
        lines(screen, WIDTH, HEIGHT, BLOCKSIZE)
        pygame.display.flip()


game()
