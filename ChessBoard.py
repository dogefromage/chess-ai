

'''
https://de.wikipedia.org/wiki/Schachprogramm
"Das Spielbrett wird auf ein eindimensionales und 120 Elemente großes Array abgebildet..."
'''

class ChessBoard:
    def __init__(self):
        self.board = [
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, #   0 to   9
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, #  10 to  19
            -1, 21, 22, 23, 24, 20, 23, 22, 21, -1, #  20 to  29
            -1,  2,  2,  2,  2,  2,  2,  2,  2, -1, #  30 to  39
            -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  40 to  49
            -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  50 to  59
            -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  60 to  69
            -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  70 to  79
            -1,  1,  1,  1,  1,  1,  1,  1,  1, -1, #  80 to  89
            -1, 11, 12, 13, 14, 10, 13, 12, 11, -1, #  90 to  99
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, # 100 to 109
            -1, -1, -1, -1, -1, -1, -1, -1, -1, -1  # 110 to 119
        ]
        self.blackKing = 25
        self.whiteKing = 95

    '''
    gets all possible moves of a single color.
    check is not considered, all possible piece moves are returned
    '''
    def generateMoves(self, isWhite):
        moves = []
        for index in range(self.board):
            square = self.board[index]
            if square <= 0: # empty
                continue
            
            if isWhite and square == 1: # white pawn
                if self.canMoveNoTake(index - 10): # forward
                    moves.append((index, index-10))
                    if index > 90 and index < 99: # is on starting field
                        if self.canMoveNoTake(index - 20):
                            moves.append((index, index-20)) # two forward, but only if one forward possible and on starting field
                if self.canMoveOnlyTake(index - 9, True): # take diagonally
                    moves.append((index, index-9))
                if self.canMoveOnlyTake(index - 11, True): # take diagonally
                    moves.append((index, index-11))

            elif not isWhite and square == 2: # black pawn
                if self.canMoveNoTake(index + 10): # forward
                    moves.append((index, index+10))
                    if index > 20 and index < 29: # is on starting field
                        if self.canMoveNoTake(index + 20):
                            moves.append((index, index+20)) # two forward, but only if one forward possible and on starting field
                if self.canMoveOnlyTake(index + 9, False): # take diagonally
                    moves.append((index, index+9))
                if self.canMoveOnlyTake(index + 11, False): # take diagonally
                    moves.append((index, index+11))

            else: # other piece
                diagonal = (-9, -11, +9, +11) # types of moves
                parallel = (-10, -1, +1, +10)
                piece = square % 10 # get piecetype 
                directions; continuous = False
                if piece == 0: # king
                    directions = parallel + diagonal
                elif piece == 1: # rook
                    directions = parallel; continuous = True
                elif piece == 2: # horse
                    directions = (-21, -19, -12, -8, +8, +12, +19, +21)
                elif piece == 3: # bishop
                    directions = diagonal; continuous = True
                elif piece == 4: # queeeeen
                    directions = parallel + diagonal; continuous = True

                for direction in directions:
                    currentIndex = index + direction
                    while self.canMove(currentIndex, isWhite):
                        moves.append((index, currentIndex))
                        if self.board[currentIndex] != 0: # if piece was hit
                            break
                        if not continuous: # if only one step possible
                            break
                        currentIndex += direction # step further in direction
                        
        return moves # return final array with all possible moves

    def standsCheck(self, othersMoves, isWhite):
        king = isWhite if self.whiteKing else self.blackKing
        for move in othersMoves:
            if king == moves[1]:
                return True
        return False

    def canMove(self, index, isWhite):
        square = self.board[index]
        if square < 0: # outside
            return False
        if square == 0: # empty field
            return True
        if square < 3: # cuck
            return isWhite == (square == 2)
        return isWhite == (square > 20) # true if piece is opposite color of "isWhite"

    def canMoveNoTake(self, index):
        square = self.board[index]
        return square == 0

    def canMoveOnlyTake(self, index, isWhite):
        square = self.board[index]
        if square == 0:
            return False
        return self.canMove(index, isWhite)


# import pygame
# from pygame.locals import *
# from ChessPieces import *

# class ChessBoard:
#     def __init__(self):
#         self.selection = (-1, -1)
#         self.badField = (-1, -1)
#         self.available = []
#         self.width = 8
#         self.height = 8
#         self.blacksTurn = False
#         self.squares = [
#             [ 'RB', 'NB', 'BB', 'QB', 'KB', 'BB', 'NB', 'RB'],
#             [ '-B', '-B', '-B', '-B', '-B', '-B', '-B', '-B'],
#             [ '',   '',   '',   '',   '',   '',   '',   '', ],
#             [ '',   '',   '',   '',   '',   '',   '',   '', ],
#             [ '',   '',   '',   '',   '',   '',   '',   '', ],
#             [ '',   '',   '',   '',   '',   '',   '',   '', ],
#             [ '-W', '-W', '-W', '-W', '-W', '-W', '-W', '-W'],
#             [ 'RW', 'NW', 'BW', 'QW', 'KW', 'BW', 'NW', 'RW']
#         ]
#         self.timeline = []
#         self.gameOver = ''

#     def draw(self, screen):
#         self.recalculateCamera(screen)
#         for j in range(self.height):
#             for i in range(self.width):
#                 screenCoords = self.BoardToScreen((i, j))
#                 rect = Rect(screenCoords, (self.scale, self.scale))
#                 # square color
#                 evenField = (i + j) % 2 == 0
#                 selectedField = self.selection == (i, j)
#                 bad = self.badField == (i, j)
                
#                 availableField = False
#                 for a in self.available:
#                     if (a == (i, j)):
#                         availableField = True
#                 color = "#ff00ff"
#                 if evenField:
#                     color = "#a3854e"
#                     if availableField:
#                         color = "#4ea36d"
#                 else:
#                     color = "#edd09a"
#                     if availableField:
#                         color = "#9aedb5"
#                 if selectedField:
#                     color = "#92c65d"
#                 if bad:
#                     color = "#cc5555"
#                 pygame.draw.rect(screen, color, rect)
#                 # piece
#                 piece = pieces.get(self.squares[j][i])
#                 if piece:
#                     screen.blit(pygame.transform.scale(piece.img, (self.scale, self.scale)), screenCoords)

#     def recalculateCamera(self, screen):
#         W, H = screen.get_size()
#         w = W - 50; h = H - 50 # margin
#         self.scale = min( int(w / self.width), int(h / self.height) )
#         self.left = (W - self.scale * self.height) * 0.5
#         self.top = (H - self.scale * self.width) * 0.5

#     def BoardToScreen(self, coords):
#         x, y = coords
#         return (int(self.left + self.scale * x), int(self.top + self.scale * y))

#     def ScreenToBoard(self, coords):
#         x, y = coords
#         return (int((x - self.left) / self.scale), int((y - self.top) / self.scale))

#     def click(self, coords):
#         self.select(self.ScreenToBoard(coords))

#     def select(self, square):
#         for a in self.available:
#             if a == square:
#                 gameState = self.move(self.selection, a)
#                 if (gameState == 'checkmate' or gameState == 'stalemate'):
#                     self.gameOver = gameState

#         # reset selection
#         if self.isInsideBoard(square):
#             self.selection = (-1, -1)
#             self.available = []
#             piece = pieces.get(self.squares[square[1]][square[0]])
#             if piece:
#                 if piece.isBlack == self.blacksTurn:
#                     self.selection = square
#                     self.available = self.findAvailableSquares(self.selection)

#     def isInsideBoard(self, coords):
#         return coords[0] >= 0 and coords[1] >= 0 and coords[0] < self.width and coords[1] < self.height

#     def findAvailableSquares(self, position, considerCheck = True):
#         available = []
#         startX, startY = position
#         piece = pieces.get(self.squares[startY][startX])
#         if (piece):
#             for move in piece.moves:
#                 x = startX; y = startY
#                 dx, dy = move[:2]
#                 if (not piece.isBlack):
#                     dy = -dy
#                 while True:
#                     x += dx; y += dy # move piece
#                     if not self.isInsideBoard((x, y)): # if not inside board
#                         break
#                     pieceAtPos = pieces.get(self.squares[y][x]) # don't take own piece
#                     if (pieceAtPos):
#                         if pieceAtPos.isBlack == piece.isBlack:
#                             break
#                     if (piece.moveStyle == 'pawn'): # cuck
#                         if move[0] == 1 or move[0] == -1: # diag. only take
#                             if not pieceAtPos:
#                                 break
#                         elif move[0] == 0: # forward no take
#                             if pieceAtPos:
#                                 break
#                             if move[1] == 2: # only 2 at beginning
#                                 if piece.isBlack:
#                                     if startY != 1: # actual y of piece
#                                         break
#                                     if self.squares[2][startX] != '': # if piece inbetween
#                                         break
#                                 else:
#                                     if startY != 6:
#                                         break
#                                     if self.squares[5][startX] != '':
#                                         break
#                     if considerCheck:
#                         self.movePiece(position, (x, y)) # check illegal move
#                         check = self.checkCheck(not self.blacksTurn)
#                         self.revertMove()
#                         if not check: # cannot ues break here because blocking check with continuous piece doesn't work
#                             available.append((x, y)) # add move to available
#                     else:
#                         available.append((x, y)) # add move to available
#                     if (piece.moveStyle == 'absolute' or piece.moveStyle == 'pawn'):  # only one move possible if absolute
#                         break
#                     if self.squares[y][x] != '': # if square is already occupied piece can't go further
#                         break
#         return available
    
#     def checkCheck(self, black):
#         king = self.findKing(black)
#         for j in range(self.height):
#             for i in range(self.width):
#                 piece = pieces.get(self.squares[j][i])
#                 if piece:
#                     if piece.isBlack != black:
#                         available = self.findAvailableSquares((i, j), False)
#                         for a in available:
#                             if king == a:
#                                 return True
#         return False

#     def findKing(self, black):
#         for j in range(self.height):
#             for i in range(self.width):
#                 square = self.squares[j][i]
#                 if black and square == 'KB':
#                     return (i, j)
#                 elif not black and square == 'KW':
#                     return (i, j)
#         return None

#     def move(self, oldPos, newPos):
#         taken = self.movePiece(oldPos, newPos)
#         # available move count
#         availableMoves = 0
#         for j in range(self.height):
#             for i in range(self.width):
#                 piece = pieces.get(self.squares[j][i])
#                 if piece:
#                     if piece.isBlack == self.blacksTurn:
#                         available = self.findAvailableSquares((i, j), True)
#                         availableMoves += len(available)
#         check = self.checkCheck(self.blacksTurn)

#         if availableMoves == 0:
#             if check:
#                 return 'checkmate'
#             else:
#                 return 'stalemate'
#         else:
#             return taken

#     def movePiece(self, oldPos, newPos):
#         ox, oy = oldPos
#         nx, ny = newPos
#         lastPiece = self.squares[ny][nx]
#         self.timeline.append((oldPos, newPos, lastPiece)) # (old, new, takes?)
#         self.squares[ny][nx] = self.squares[oy][ox]
#         self.squares[oy][ox] = ''
#         self.blacksTurn = not self.blacksTurn
#         return lastPiece

#     def revertMove(self):
#         action = self.timeline.pop(-1)
#         ox, oy = action[0]
#         nx, ny = action[1]
#         self.squares[oy][ox] = self.squares[ny][nx]
#         self.squares[ny][nx] = action[2]
#         self.blacksTurn = not self.blacksTurn
