import sys
import pygame
import time
import math

class Conway(object):

    def surrounding(self, x, y, squares, w, h):
        """Returns the number of adjacent cells to the (x, y) provided."""
        surrounding = 0

        adjacent_squares = (
            (x-1, y-1),
            (x-1, y),
            (x, y-1),
            (x+1, y),
            (x, y+1),
            (x+1, y+1),
            (x+1, y-1),
            (x-1, y+1)
        )

        for square in adjacent_squares:
            x = square[0]
            y = square[1]
            if (self.in_bounds(x, y, w, h)):
                # if that adjacent cell is alive
                if (squares[x][y]):
                    surrounding += 1
        return surrounding

    def in_bounds(self, x, y, w, h):
        """Returns True if the cell is in the bounds of the given width and
        height."""
        if (x >= 0 and x <= w-1 and y <= h-1 and y >= 0):
            return True
        return False

    def get_state(self, state, surrounding_cells):
        """Returns the proper next state of a cell given it's current state
        and surroudning cells."""
        # alive
        if state == True:
            if (surrounding_cells == 2 or surrounding_cells == 3):
                return True
            else:
                return False
        # dead
        else:
            if (surrounding_cells == 3):
                return True
            else:
                return False
        return False

    def clear_board(self, w, h):
        """Returns an empty board"""
        board = []
        for i in range(0, w):
            board.append([])
            for j in range(0, h):
                board[i].append(False)
        return board

    def next_board(self, board, w, h):
        """Returns the next proper board given a current state"""
        new = []
        new = self.clear_board(w, h)
        for i in range(0, w):
            for j in range(0, h):
                surround = self.surrounding(i, j, board, w, h)
                state = board[i][j]
                new[i][j] = self.get_state(state, surround)
        return new

    def __init__(self):
        # initialize pygame
        pygame.init()

        cell_w = 100
        cell_h = 60
        size = width, height = cell_w*10, cell_h*10
        black = 0, 0, 0
        last_refresh = time.time()
        squares = []
        bsquares = []
        animate = False

        squares = self.clear_board(cell_w, cell_h)
        bsquares = self.clear_board(cell_w, cell_h)

        # create a window the desired size
        screen = pygame.display.set_mode(size)
        # load the square images
        dead_square = pygame.image.load("square.jpg")
        alive_square = pygame.image.load("alive.jpg")

        while True:
            if (animate == True):
                refresh_rate = .0
            else:
                refresh_rate = 0

            # exit on exit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # toggle mode
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                # toggle animate
                animate = not animate
                # sleep to prevent bouncing
                time.sleep(.1)

            # delete cells
            if pygame.key.get_pressed()[pygame.K_DELETE]:
                squares = bsquares = self.clear_board(cell_w, cell_h)
                time.sleep(.1)

            # code for inputting alive cells
            if (animate == False):
                # clicking
                if pygame.mouse.get_pressed()[0]:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    x = int(x/10)
                    y = int(y/10)
                    # change value of square
                    squares[x][y] = True

            # code for animating the cells
            elif (animate == True):
                bsquares = self.next_board(squares, cell_w, cell_h)
                squares = bsquares
                bsquares = self.clear_board(cell_w, cell_h)

            # wait for time interval (100 fps)
            if (time.time() - last_refresh < refresh_rate):
                continue
            else:
                last_refresh = time.time()

            # blank screen
            screen.fill(black)
            # draw squares

            for i in range(0, cell_w):
                for j in range(0, cell_h):
                    if (squares[i][j] == False):
                        screen.blit(dead_square,
                            (i*10, j*10, 10, 10))
                    else:
                        screen.blit(alive_square,
                            (i*10, j*10, 10, 10))
            # flip buffer
            pygame.display.flip()

c = Conway()
