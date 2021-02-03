from ChessPieces import *
import random

class ChessAI:
    def __init__(self, maxDepth, isBlack):
        self.maxDepth = maxDepth
        self.isBlack = isBlack

    def play(self, board):
        old, new = self.minimax(board, True, 0)
        board.move(old, new)

    def minimax(self, board, maximizingPlayer, depth):
        for j in range(board.height):
            for i in range(board.width):
                piece = pieces.get(board.squares[j][i])
                if piece:
                    if piece.isBlack == maximizingPlayer:
                        available = board.findAvailableSquares((i, j), True)
                        if (available > 0)
                        if (maximizingPlayer):
                            maxScore = -1000000000000000
                            status = board.move()

        # olds = []
        # for j in range(board.height):
        #     for i in range(board.width):
        #         piece = pieces.get(board.squares[j][i])
        #         if piece:
        #             if piece.isBlack == self.isBlack:
        #                 available = board.findAvailableSquares((i, j))
        #                 if len(available) > 0:
        #                     olds.append((i, j, available))
        # index1 = random.randrange(0,len(olds))
        # old = olds[index1]
        # index2 = random.randrange(0, len(old[2]))
        # new = old[2][index2]
        # return (old[:2], new)