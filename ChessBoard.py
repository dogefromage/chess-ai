import pygame
from pygame.locals import *
from ChessPieces import *

class ChessBoard:
    def __init__(self):
        self.selection = (-1, -1)
        self.illegalField = (-1, -1)
        self.available = []
        self.width = 8
        self.height = 8
        self.blacksTurn = False
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
        self.timeline = []

    def draw(self, screen):
        self.recalculateCamera(screen)
        for j in range(self.height):
            for i in range(self.width):
                screenCoords = self.BoardToScreen((i, j))
                rect = Rect(screenCoords, (self.scale, self.scale))

                # square color
                evenField = (i + j) % 2 == 0
                selectedField = self.selection == (i, j)
                illegal = self.illegalField == (i, j)
                
                availableField = False
                for a in self.available:
                    if (a == (i, j)):
                        availableField = True
                color = "#ff00ff"
                if evenField:
                    color = "#a3854e"
                    if availableField:
                        # color = "#a3594e"
                        color = "#4ea36d"
                else:
                    color = "#edd09a"
                    if availableField:
                        color = "#9aedb5" #"#eda79a"
                if selectedField:
                    color = "#92c65d"
                if illegal:
                    color = "#cc5555"



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
        self.select(self.ScreenToBoard(coords))

    def select(self, square):
        for a in self.available:
            if a[0] == square[0] and a[1] == square[1]:
                self.choose(self.selection, a)
        # reset selection
        self.selection = (-1, -1)
        self.available = []
        if self.isInsideBoard(square):
            piece = pieces.get(self.squares[square[1]][square[0]])
            if piece:
                if piece.isBlack == self.blacksTurn:
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
                dx, dy = move[:2]
                if (not piece.isBlack):
                    dy = -dy
                while True:
                    x += dx; y += dy # move piece

                    if not self.isInsideBoard((x, y)): # if not inside board
                        break

                    pieceAtPos = pieces.get(self.squares[y][x]) # don't take own piece
                    if (pieceAtPos):
                        if pieceAtPos.isBlack == piece.isBlack:
                            break
                    
                    if (piece.moveStyle == 'pawn'): # cuck
                        if move[0] == 1 or move[0] == -1: # diag. only take
                            if not pieceAtPos:
                                break
                        elif move[0] == 0: # forward no take
                            if pieceAtPos:
                                break
                            if move[1] == 2: # only 2 at beginning
                                if piece.isBlack:
                                    if self.selection[1] != 1: # actual y of piece
                                        break
                                else:
                                    if self.selection[1] != 6:
                                        break

                    self.available.append((x, y)) # add move to available
                   
                    if (piece.moveStyle == 'absolute' or piece.moveStyle == 'pawn'):  # only one move possible if absolute
                        break
                    if self.squares[y][x] != '': # if square is already occupied piece can't go further
                        break

    def getAllPieceLocations(self, isBlack):
        locations = []
        for j in range(self.height):
            for i in range(self.width):
                square = self.squares[j][i]
                if square != '':
                    if (square[1] == 'B') == isBlack:
                        locations.append((i, j))
        return locations

    def findKing(self, isBlack):
        for j in range(self.height):
            for i in range(self.width):
                square = self.squares[j][i]
                if isBlack and square == 'KB':
                    return (i, j)
                elif not isBlack and square == 'KW':
                    return (i, j)

    def checkCheck(self, isBlack):
        locations = self.getAllPieceLocations(isBlack)
        king = self.findKing(not isBlack)
        oldSelection = self.selection
        oldAvailable = self.available
        for location in locations:
            self.selection = location
            self.findAvailableSquares()
            for a in self.available:
                if king == a:
                    return True
        self.selection = oldSelection
        self.available = oldAvailable
        return False

    def choose(self, oldPos, newPos):
        self.move(oldPos, newPos)
        # check illegal move
        check = self.checkCheck(self.blacksTurn)
        if check:
            self.revert()
            self.illegalField = newPos
        else:
            self.illegalField = (-1, -1)
        # check checkmate

    def move(self, oldPos, newPos):
        ox, oy = oldPos
        nx, ny = newPos
        self.timeline.append((oldPos, newPos, self.squares[ny][nx])) # (old, new, takes?)
        self.squares[ny][nx] = self.squares[oy][ox]
        self.squares[oy][ox] = ''
        self.blacksTurn = not self.blacksTurn

    def revert(self):
        action = self.timeline.pop(-1)
        ox, oy = action[0]
        nx, ny = action[1]
        self.squares[oy][ox] = self.squares[ny][nx]
        self.squares[ny][nx] = action[2]
        self.blacksTurn = not self.blacksTurn
        # move back
