from ChessBoard import ChessBoard

class ChessAI:
    def __init__(self, maxDepth = 4, isBlack = True):
        self.maxDepth = maxDepth
        self.isBlack = isBlack
 
    def play(self, board):
        return self.minimax(board, True, 0)[0] # return only move

    def minimax(self, board, maximizingPlayer, currentDepth):
        if (currentDepth == self.maxDepth):
            return (None, self.staticEval(board))
        if maximizingPlayer:
            bestMove = None; bestScore = -100000
            for piece in board.moves:
                for m in board.moves[piece]:
                    boardCopy = ChessBoard(board) # replace with copy
                    action = boardCopy.move(piece, m)
                    if action < 0: # move illegal
                        continue
                    # throw away move, only score needed
                    _, score = self.minimax(boardCopy, False, currentDepth + 1)
                    if action == 1 or action == 2:
                        score += 1 # eaten peasant
                    else:
                        action %= 10
                        if action == 1:
                            score += 5 # rook
                        elif action == 2 or action == 3:
                            score += 3 # horse / bishop
                        elif action == 4:
                            score += 9 # queen
                    if score > bestScore:
                        bestScore = score
                        bestMove = (piece, m)
            return (bestMove, bestScore)
        else:
            worstMove = None; worstScore = 100000
            for piece in board.moves:
                for m in board.moves[piece]:
                    boardCopy = ChessBoard(board) # replace with copy
                    action = boardCopy.move(piece, m)
                    if action < 0: # move illegal
                        continue
                    # throw away move, only score needed
                    _, score = self.minimax(boardCopy, True, currentDepth + 1)
                    if action == 1 or action == 2:
                        score -= 1 # eaten peasant
                    else:
                        action %= 10
                        if action == 1:
                            score -= 5 # rook
                        elif action == 2 or action == 3:
                            score -= 3 # horse / bishop
                        elif action == 4:
                            score -= 9 # queen
                    if score > worstScore:
                        worstScore = score
                        worstMove = (piece, m)
            return (worstMove, worstScore)


    def staticEval(self, board):
        return 0