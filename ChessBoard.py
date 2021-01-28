import pygame
from pygame.locals import *
from ChessPieces import *

class ChessBoard:
    def __init__(self):
        self.selection = (-1, -1)
        self.available = []
        self.width = 8
        self.height = 8
        self.squares = [
            [ 'RB', 'NB', 'BB', 'QB', 'KB', 'BB', 'NB', 'RB'],
            [ '-B', '-B', '-B', '-B', '-B', '-B', '-B', '-B'],
            [ '',   '',   '',   '',   '',   '',   '',   '', ],
            [ '',   '',   '',   '',   '',   '',   '',   '', ],
            [ '',   '',   '',   '',   '',   '',   '',   '', ],
            [ '',   '',   '',   '',   '',   '',   '',   '', ],
            [ '-W', '-W', '-W', '-W', '-W', '-W', '-W', '-W'],
            [ 'RW', 'NW', 'BW', 'QW', 'KW', 'BW', 'NW', 'RW']
        ]

    def draw(self, screen):
        self.recalculateCamera(screen)

        for j in range(self.height):
            for i in range(self.width):
                # square color
                screenCoords = self.BoardToScreen((i, j))
                rect = Rect(screenCoords, (self.scale, self.scale))
                color = "#a3854e"
                if ((i + j) % 2 == 0):
                    color = "#edd09a"
                if (self.selection[0] == i and self.selection[1] == j):
                    color = "#ff0000"
                for a in self.available:
                    if (a[0] == i and a[1] == j):
                        color = "#00ff00"

                pygame.draw.rect(screen, color, rect)
                # piece
                piece = pieces.get(self.squares[j][i])
                if piece:
                    screen.blit(pygame.transform.scale(piece.img, (self.scale, self.scale)), screenCoords)

    def recalculateCamera(self, screen):
        W, H = screen.get_size()
        w = W - 50; h = H - 50 # margin
        self.scale = min( int(w / self.width), int(h / self.height) )
        self.left = (W - self.scale * self.height) * 0.5
        self.top = (H - self.scale * self.width) * 0.5

    def BoardToScreen(self, coords):
        x, y = coords
        return (int(self.left + self.scale * x), int(self.top + self.scale * y))

    def ScreenToBoard(self, coords):
        x, y = coords
        return (int((x - self.left) / self.scale), int((y - self.top) / self.scale))

    def click(self, coords):
        square = self.ScreenToBoard(coords)
        for a in self.available:
            if a[0] == square[0] and a[1] == square[1]:
                self.movePiece(self.selection, a)
                self.selection = (-1, -1)
                self.available = []
                return

        # else do this
        if (self.isInsideBoard(square)):
            self.selection = square
            self.findAvailableSquares()

    def isInsideBoard(self, coords):
        return coords[0] >= 0 and coords[1] >= 0 and coords[0] < self.width and coords[1] < self.height

    def findAvailableSquares(self):
        self.available = []
        x, y = self.selection
        piece = pieces.get(self.squares[y][x])
        if (piece):
            for move in piece.moves:
                x, y = self.selection
                dx, dy = move
                if (not piece.isBlack):
                    dy = -dy
                while True:
                    x += dx
                    y += dy
                    if not self.isInsideBoard((x, y)):
                        break
                    # don't take own piece
                    pieceAtPos = pieces.get(self.squares[y][x])
                    if (pieceAtPos):
                        if pieceAtPos.isBlack == piece.isBlack:
                            break
                    self.available.append((x, y))
                    if (piece.moveStyle == 'absolute'): # only one move
                        break
                    if self.squares[y][x] != '':
                        break

    def movePiece(self, lastPos, newPos):
        if not self.isInsideBoard(lastPos):
            return
        if not self.isInsideBoard(newPos):
            return
        ox, oy = lastPos
        nx, ny = newPos
        piece = self.squares[oy][ox]
        if piece == '':
            return
        self.squares[ny][nx] = piece
        self.squares[oy][ox] = ''

