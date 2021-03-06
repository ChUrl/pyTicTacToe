#!/usr/bin/env python3

import pygame
from copy import copy, deepcopy
from rich.traceback import install

install()
pygame.init()

# Constants
ICON_SIZE = 128
PADDING = 8
SIZE = 3 * ICON_SIZE + 4 * PADDING

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Setup
blue = pygame.image.load("BlueCircle.png")
red = pygame.image.load("RedSquare.png")

clock = pygame.time.Clock()
logo = pygame.image.load("BlueCircle.png")
screen = pygame.display.set_mode((SIZE, SIZE))

pygame.display.set_caption("TicTacToe")
pygame.display.set_icon(logo)
print()


# State
turn = 1 # 1: RED, -1: BLUE
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
score = [0, 0, 0, 0, 0, 0, 0, 0]
depth = 1


# Functions
def draw_board(board: list[list[int]]):
    screen.fill(WHITE)

    # Horizontal Grid
    pygame.draw.rect(screen, BLACK, (0, 0, SIZE, PADDING))
    pygame.draw.rect(screen, BLACK, (0, 136, SIZE, PADDING))
    pygame.draw.rect(screen, BLACK, (0, 270, SIZE, PADDING))
    pygame.draw.rect(screen, BLACK, (0, 408, SIZE, PADDING))

    # Vertical Grid
    pygame.draw.rect(screen, BLACK, (0, 0, PADDING, SIZE))
    pygame.draw.rect(screen, BLACK, (136, 0, PADDING, SIZE))
    pygame.draw.rect(screen, BLACK, (270, 0, PADDING, SIZE))
    pygame.draw.rect(screen, BLACK, (408, 0, PADDING, SIZE))

    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                screen.blit(red, get_quadrant_position(i, j))
            elif board[i][j] == -1:
                screen.blit(blue, get_quadrant_position(i, j))


def get_quadrant_position(i: int, j: int) -> tuple[float, float]:
    """
    Ermittelt den Ursprung (obere linke Ecke) des Quadranten in Zeile i und Spalte j.
    """
    x = PADDING + j * (ICON_SIZE + PADDING)
    y = PADDING + i * (ICON_SIZE + PADDING)

    return (x, y)


def get_mouse_quadrant(pos: tuple[float, float]) -> tuple[int, int]:
    """
    Ermittelt die Zeile i und Spalte j des Quadranten anhand der x- und y-Koordinaten des Mauszeigers.
    """
    x, y = pos
    i = int((y - 8) // (ICON_SIZE + PADDING))
    j = int((x - 8) // (ICON_SIZE + PADDING))

    return (i, j)


def update_board(i: int, j: int, board: list[list[int]], turn: int) -> list[list[int]]:
    board = deepcopy(board)
    board[i][j] = turn

    return board


def update_score(i: int, j: int, score: list[int], turn: int) -> list[int]:
    """
    Fügt der Score-Tabelle die richtigen Einträge hinzu.
    """
    score = copy(score)
    score[i] += turn
    score[3 + j] += turn

    if i - j == 0:
        score[6] += turn
    if i + j == 2:
        score[7] += turn

    return score


def rate_score(score: list[int]) -> tuple[int, int]:
    red = sum(s for s in score if s > 0)
    blue = sum(s for s in score if s < 0)

    if max(score) == 2:
        red = 1000
    if min(score) == -2:
        blue = -1000

    return (red, blue)


def eval_best_move(board: list[list[int]], score: list[int], turn: int) -> tuple[int, int]:
    ij, rating = (0, 0), (0, 0)
    board = deepcopy(board)
    score = copy(score)

    if d > depth:
        return (-1, -1)

    print(f"Turn {turn}:", "Red" if turn > 0 else "Blue")

    for i in range(3):
        for j in range(3):
            if not turn_is_valid(i, j, board):
                continue

            s = update_score(i, j, score, turn)
            r = rate_score(s)

            print(f" :: Move ({i}, {j}) has rating {r}.")

            if turn > 0 and sum(r) > sum(rating):
                ij, rating = (i, j), r
            elif turn < 0 and sum(r) < sum(rating):
                ij, rating = (i, j), r

    print(f"Chose move {ij} with rating {rating} = {sum(rating)}")

    return ij


def turn_is_valid(i: int, j: int, board: list[list[int]]) -> bool:
    return board[i][j] == 0


def do_turn(pos: tuple[float, float], board: list[list[int]], score: list[int], turn: int) -> tuple[list[list[int]], list[int], int]:
    board = deepcopy(board)
    score = copy(score)
    i, j = get_mouse_quadrant(pos)

    if turn_is_valid(i, j, board):
        board = update_board(i, j, board, turn)
        score = update_score(i, j, score, turn)

        return board, score, turn * -1

    print("Invalid Turn.")
    return board, score, turn


def check_win(score: list[int]) -> bool:
    if min(score) == -3:
        print("BLUE Wins")
        return True

    if max(score) == 3:
        print("RED Wins")
        return True

    return False


def board_is_full(board: list[list[int]]):
    board_sum = sum([sum(abs(cell) for cell in row) for row in board])

    if board_sum == 9:
        print("Game Over")
        return True

    return False



# Loop
running = True
while running:

    # Input
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            board, score, turn = do_turn(pygame.mouse.get_pos(), board, score, turn)

            # print(score, ":" ,rate_score(score))
            # print("Best Move:", eval_best_move(board, score))
            eval_best_move(board, score, turn)

            running = not check_win(score) and not board_is_full(board)

    # Render
    draw_board(board)
    pygame.display.flip()
    # pygame.display.update() # Double Buffering?

    clock.tick(15)


pygame.quit()
