import pygame
from pygame.locals import *
from ChessPieces import *

class ChessBoard:
    def __init__(self):
        self.selection = (-1, -1)
        self.badField = (-1, -1)
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
        self.gameOver = ''

    def draw(self, screen):
        self.recalculateCamera(screen)
        for j in range(self.height):
            for i in range(self.width):
                screenCoords = self.BoardToScreen((i, j))
                rect = Rect(screenCoords, (self.scale, self.scale))
                # square color
                evenField = (i + j) % 2 == 0
                selectedField = self.selection == (i, j)
                bad = self.badField == (i, j)
                
                availableField = False
                for a in self.available:
                    if (a == (i, j)):
                        availableField = True
                color = "#ff00ff"
                if evenField:
                    color = "#a3854e"
                    if availableField:
                        color = "#4ea36d"
                else:
                    color = "#edd09a"
                    if availableField:
                        color = "#9aedb5"
                if selectedField:
                    color = "#92c65d"
                if bad:
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
            if a == square:
                gameState = self.move(self.selection, a)
                if (gameState == 'checkmate' or gameState == 'stalemate'):
                    self.gameOver = gameState

        # reset selection
        if self.isInsideBoard(square):
            self.selection = (-1, -1)
            self.available = []
            piece = pieces.get(self.squares[square[1]][square[0]])
            if piece:
                if piece.isBlack == self.blacksTurn:
                    self.selection = square
                    self.available = self.findAvailableSquares(self.selection)

    def isInsideBoard(self, coords):
        return coords[0] >= 0 and coords[1] >= 0 and coords[0] < self.width and coords[1] < self.height

    def findAvailableSquares(self, position, considerCheck = True):
        available = []
        startX, startY = position
        piece = pieces.get(self.squares[startY][startX])
        if (piece):
            for move in piece.moves:
                x = startX; y = startY
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
                                    if startY != 1: # actual y of piece
                                        break
                                    if self.squares[2][startX] != '': # if piece inbetween
                                        break
                                else:
                                    if startY != 6:
                                        break
                                    if self.squares[5][startX] != '':
                                        break
                    if considerCheck:
                        self.movePiece(position, (x, y)) # check illegal move
                        check = self.checkCheck(not self.blacksTurn)
                        self.revertMove()
                        if not check: # cannot ues break here because blocking check with continuous piece doesn't work
                            available.append((x, y)) # add move to available
                    else:
                        available.append((x, y)) # add move to available
                    if (piece.moveStyle == 'absolute' or piece.moveStyle == 'pawn'):  # only one move possible if absolute
                        break
                    if self.squares[y][x] != '': # if square is already occupied piece can't go further
                        break
        return available
    
    def checkCheck(self, black):
        king = self.findKing(black)
        for j in range(self.height):
            for i in range(self.width):
                piece = pieces.get(self.squares[j][i])
                if piece:
                    if piece.isBlack != black:
                        available = self.findAvailableSquares((i, j), False)
                        for a in available:
                            if king == a:
                                return True
        return False

    def findKing(self, black):
        for j in range(self.height):
            for i in range(self.width):
                square = self.squares[j][i]
                if black and square == 'KB':
                    return (i, j)
                elif not black and square == 'KW':
                    return (i, j)
        return None

    def move(self, oldPos, newPos):
        taken = self.movePiece(oldPos, newPos)
        # available move count
        availableMoves = 0
        for j in range(self.height):
            for i in range(self.width):
                piece = pieces.get(self.squares[j][i])
                if piece:
                    if piece.isBlack == self.blacksTurn:
                        available = self.findAvailableSquares((i, j), True)
                        availableMoves += len(available)
        check = self.checkCheck(self.blacksTurn)

        if availableMoves == 0:
            if check:
                return 'checkmate'
            else:
                return 'stalemate'
        else:
            return taken

    def movePiece(self, oldPos, newPos):
        ox, oy = oldPos
        nx, ny = newPos
        lastPiece = self.squares[ny][nx]
        self.timeline.append((oldPos, newPos, lastPiece)) # (old, new, takes?)
        self.squares[ny][nx] = self.squares[oy][ox]
        self.squares[oy][ox] = ''
        self.blacksTurn = not self.blacksTurn
        return lastPiece

    def revertMove(self):
        action = self.timeline.pop(-1)
        ox, oy = action[0]
        nx, ny = action[1]
        self.squares[oy][ox] = self.squares[ny][nx]
        self.squares[ny][nx] = action[2]
        self.blacksTurn = not self.blacksTurn
