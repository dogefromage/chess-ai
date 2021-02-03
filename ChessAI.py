from ChessPieces import *
import random

class ChessAI:
    def __init__(self, maxDepth, isBlack):
        self.maxDepth = maxDepth

    def play(self, board):
        old, new = self.minimax(board, True, 0)
        board.move(old, new)

    def minimax(self, board, maximizingPlayer, depth):

        for j in range(board.height):
            for i in range(board.width):
                piece = pieces.get(board.squares[j][i])
                if piece:
                    if piece.isBlack == maximizingPlayer:
                        board.selection = (i, j)
                        board.findAvailableSquares(True)
                        if (maximizingPlayer):
                            maxScore = 
                        score = board.move()










        # RANDOM
        # olds = []
        # for j in range(board.height):
        #     for i in range(board.width):
        #         piece = pieces.get(board.squares[j][i])
        #         if piece:
        #             if piece.isBlack == self.isBlack:
        #                 board.selection = (i, j)
        #                 board.findAvailableSquares()
        #                 if len(board.available) > 0:
        #                     olds.append((i, j, board.available))
        # index1 = random.randrange(0,len(olds))
        # old = olds[index1]
        # index2 = random.randrange(0, len(old[2]))
        # new = old[2][index2]
        # board.selection = (-1, -1)
        # return (old[:2], new)