from Evaluation import *

def getWeight(e):
    return e[2]

'''
https://de.wikipedia.org/wiki/Schachprogramm
"Das Spielbrett wird auf ein eindimensionales und 120 Elemente großes Array abgebildet..."
'''
class ChessBoard:
    def __init__(self, boardToCopy = None):
        if boardToCopy:
            ''' 
            copy
            '''
            self.board = [ x for x in boardToCopy.board ] # copy board
            self.blackKing = boardToCopy.blackKing
            self.whiteKing = boardToCopy.whiteKing
            self.whitesTurn = boardToCopy.whitesTurn
            # self.castleNearWhite = boardToCopy.castleNearWhite
            # self.castleFarWhite = boardToCopy.castleFarWhite
            # self.castleNearBlack = boardToCopy.castleNearBlack
            # self.castleFarBlack = boardToCopy.castleFarBlack
        else:
            '''
            create new
            '''
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
            self.findKings()
            # self.board = [
            #     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, #   0 to   9
            #     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, #  10 to  19
            #     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  40 to  49
            #     -1,  0,  1,  0,  0,  0,  0,  0,  0, -1, #  40 to  49
            #     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  40 to  49
            #     -1,  1,  0,  0,  0,  0,  0,  0,  0, -1, #  40 to  49
            #     -1,  0,  0,  0,  0,  0,  0,  0,  20, -1, #  40 to  49
            #     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  50 to  59
            #     -1,  0,  0,  0,  0,  0,  0,  0,  0, -1, #  60 to  69
            #     -1,  0,  0,  0,  0,  0,  0,  10,  0, -1, #  70 to  79
            #     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, # 100 to 109
            #     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1  # 110 to 119
            # ]
            # self.findKings()
            self.whitesTurn = True
            # # CHASTLING STILL POSSIBLE?
            # self.castleNearWhite = False
            # self.castleFarWhite = False
            # self.castleNearBlack = False
            # self.castleFarBlack = False

        self.history = []
        self.moves = self.generateMoves(self.whitesTurn) # pseudo moves, not all are valid but this is fastest

    '''
    gets all possible moves of a single color.
    check is not considered, all possible piece moves are returned
    every move gets a importance, important moves are put earlier into list to improve alpha-beta pruning
    '''

    def generateMoves(self, isWhite, weighted=True):
        moves = [] # list of possible moves (weighted by d)
        for index in range(len(self.board)):
            moves += self.generatePieceMoves(index, isWhite, weighted)
        moves.sort(key=getWeight, reverse=isWhite)
        moves = [ move[0:2] for move in moves ]
        return moves # return final dic with lists of all possible moves

    def generatePieceMoves(self, index, isWhite, weighted=True):
        square = self.board[index]
        if square <= 0: # empty
            return []
        pieceMoves = [] # list of moves for this piece
        if isWhite and square == 1: # white pawn
            if self.canMoveNoTake(index - 10): # forward
                pieceMoves.append(index-10)
                if index > 80 and index < 89: # is on starting field
                    if self.canMoveNoTake(index - 20):
                        pieceMoves.append(index-20) # two forward, but only if one forward possible and on starting field
            if self.canMoveOnlyTake(index - 9, True): # take diagonally
                pieceMoves.append(index-9)
            if self.canMoveOnlyTake(index - 11, True): # take diagonally
                pieceMoves.append(index-11)

        elif not isWhite and square == 2: # black pawn
            if self.canMoveNoTake(index + 10): # forward
                pieceMoves.append(index+10)
                if index > 30 and index < 39: # is on starting field
                    if self.canMoveNoTake(index + 20):
                        pieceMoves.append(index+20) # two forward, but only if one forward possible and on starting field
            if self.canMoveOnlyTake(index + 9, False): # take diagonally
                pieceMoves.append(index+9)
            if self.canMoveOnlyTake(index + 11, False): # take diagonally
                pieceMoves.append(index+11)

        elif square > 2 and (square < 20) == isWhite: # other pieces of the players color
            diagonal = (-9, -11, +9, +11) # types of moves
            parallel = (-10, -1, +1, +10)
            piece = square % 10 # get piecetype 
            directions = None; continuous = False
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
                    pieceMoves.append(currentIndex)
                    if self.board[currentIndex] != 0: # if piece was hit
                        break
                    if not continuous: # if only one step possible
                        break
                    currentIndex += direction # step further in direction
        # if weighted:
        #     weightedMoves = []
        #     for move in pieceMoves:
        #         action = self.move(index, move, False)
        #         if action >= 0:
        #             score = evaluate(self)
        #             self.takeBack()
        #             weightedMoves.append((index, move, score))
        #     return weightedMoves
        # else:
        return [ (index, move, 0) for move in pieceMoves ]

    def canMove(self, index, isWhite):
        square = self.board[index]
        if square < 0: # outside
            return False
        if square == 0: # empty field
            return True
        if square < 3: # cuck
            return isWhite == (square == 2)
        pieceisBlack = (square >= 20)
        return isWhite == pieceisBlack # true if piece is opposite color of "isWhite"

    def canMoveNoTake(self, index):
        square = self.board[index]
        return square == 0

    def canMoveOnlyTake(self, index, isWhite):
        square = self.board[index]
        if square == 0:
            return False
        return self.canMove(index, isWhite)

#    def generateMoves(self, isWhite):
#         moves = {} # dictionary of possible moves
#         possibleMoveCount = 0
#         for index in range(len(self.board)):
#             pieceMoves = self.generatePieceMoves(index, isWhite)
#             if len(pieceMoves) > 0:
#                 moves[index] = pieceMoves # save moves in dic
#                 possibleMoveCount += len(pieceMoves)
#         return (moves, possibleMoveCount) # return final dic with lists of all possible moves

#     def generatePieceMoves(self, index, isWhite):
#         square = self.board[index]
#         if square <= 0: # empty
#             return []
#         pieceMoves = [] # list of moves for this piece
#         if isWhite and square == 1: # white pawn
#             if self.canMoveNoTake(index - 10): # forward
#                 pieceMoves.append(index-10)
#                 if index > 80 and index < 89: # is on starting field
#                     if self.canMoveNoTake(index - 20):
#                         pieceMoves.append(index-20) # two forward, but only if one forward possible and on starting field
#             if self.canMoveOnlyTake(index - 9, True): # take diagonally
#                 pieceMoves.append(index-9)
#             if self.canMoveOnlyTake(index - 11, True): # take diagonally
#                 pieceMoves.append(index-11)

#         elif not isWhite and square == 2: # black pawn
#             if self.canMoveNoTake(index + 10): # forward
#                 pieceMoves.append(index+10)
#                 if index > 30 and index < 39: # is on starting field
#                     if self.canMoveNoTake(index + 20):
#                         pieceMoves.append(index+20) # two forward, but only if one forward possible and on starting field
#             if self.canMoveOnlyTake(index + 9, False): # take diagonally
#                 pieceMoves.append(index+9)
#             if self.canMoveOnlyTake(index + 11, False): # take diagonally
#                 pieceMoves.append(index+11)

#         elif square > 2 and (square < 20) == isWhite: # other pieces of the players color
#             diagonal = (-9, -11, +9, +11) # types of moves
#             parallel = (-10, -1, +1, +10)
#             piece = square % 10 # get piecetype 
#             directions = None; continuous = False
#             if piece == 0: # king
#                 directions = parallel + diagonal
#             elif piece == 1: # rook
#                 directions = parallel; continuous = True
#             elif piece == 2: # horse
#                 directions = (-21, -19, -12, -8, +8, +12, +19, +21)
#             elif piece == 3: # bishop
#                 directions = diagonal; continuous = True
#             elif piece == 4: # queeeeen
#                 directions = parallel + diagonal; continuous = True

#             for direction in directions:
#                 currentIndex = index + direction
#                 while self.canMove(currentIndex, isWhite):
#                     pieceMoves.append(currentIndex)
#                     if self.board[currentIndex] != 0: # if piece was hit
#                         break
#                     if not continuous: # if only one step possible
#                         break
#                     currentIndex += direction # step further in direction
#         return pieceMoves

#     def canMove(self, index, isWhite):
#         square = self.board[index]
#         if square < 0: # outside
#             return False
#         if square == 0: # empty field
#             return True
#         if square < 3: # cuck
#             return isWhite == (square == 2)
#         pieceisBlack = (square >= 20)
#         return isWhite == pieceisBlack # true if piece is opposite color of "isWhite"

#     def canMoveNoTake(self, index):
#         square = self.board[index]
#         return square == 0

#     def canMoveOnlyTake(self, index, isWhite):
#         square = self.board[index]
#         if square == 0:
#             return False
#         return self.canMove(index, isWhite)

    def findKings(self):
        for square in self.board:
            if square == 10:
                self.whiteKing = square
            elif square == 20:
                self.blackKing = square

    def setTurn(self, isWhite, weightNextMoves = True):
        self.whitesTurn = isWhite
        self.moves = self.generateMoves(isWhite, weightNextMoves)

    def move(self, last, new, weightNextMoves = True):
        changes = {} # records changes to board at certain position, only necessary bc. promotions, castling, enpassant :(
        piece = self.board[last]
        if piece <= 0:
            return -1 # invalid
        taken = self.board[new]
        self.board[new] = self.board[last]
        self.board[last] = 0
        changes[last] = (piece, 0) # last square changed from piece to empty
        changes[new] = (taken, piece) # new square changed from taken space to the piece
        # promotion
        if piece == 1:
            if new > 20 and new < 29:
                self.board[new] = 14
                changes[new] = (changes[new][0], 14) # override change to queen 
        elif piece == 2:
            if new > 90 and new < 99:
                self.board[new] = 24
                changes[new] = (changes[new][0], 24) # override change to queen 
        # update kings pos
        if piece == 10:
            self.whiteKing = new
        elif piece == 20:
            self.blackKing = new
        # write history
        self.history.append(changes)
        # flip turns and generate new moves
        self.setTurn(not self.whitesTurn, weightNextMoves)
        '''
        find out if king in check and therefore illegal move.
        If he is, take back move and return -1
        '''
        king = self.blackKing if self.whitesTurn else self.whiteKing
        for move in self.moves:
            if king == move[1]:  # walked into check = illegal
                self.takeBack()
                return -1 # illegal

        return taken # for fitness function (if needed)

    '''
    SLOW! only call if necessary (only after every REAL turn not simulated)
    '''
    def getGameState(self):
        '''
        attempt to execute every next "pseudo move" and count the valid ones
        '''
        validMoves = 0
        for move in self.moves:
            result = self.move(move[0], move[1])
            if result >= 0: # move is valid
                self.takeBack()
                validMoves += 1
        if validMoves == 0:
            check = self.standsCheck(self.whitesTurn)
            if check:
                if self.whitesTurn:
                    return ("Checkmate, Black won", True)
                else:
                    return ("Checkmate, White won", True)
            else:
                return ("Stalemate", True)
        else:
            if self.whitesTurn:
                return ("White to move", False)
            else:
                return ("Black to move", False)
 
    def standsCheck(self, isWhite):
        king = self.whiteKing if isWhite else self.blackKing
        testBoard = ChessBoard(self) # making a copy simplest
        testBoard.setTurn(not isWhite)
        for move in testBoard.moves:
            if move[1] == king:
                return True
        return False

    def takeBack(self):
        if len(self.history) == 0:
            return
        action = self.history.pop(-1)
        for square in action:
            piece = action[square][0]
            self.board[square] = piece # change square back
            # update kings
            if piece == 10:
                self.whiteKing = square
            elif piece == 20:
                self.blackKing = square
        # flip turns and generate new moves
        self.setTurn(not self.whitesTurn)

    def getAvailable(self, index):
        available = []
        for move in self.moves:
            if move[0] == index:
                available.append(move[1])
        return available
