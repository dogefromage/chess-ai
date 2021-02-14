from ChessBoard import ChessBoard
from Evaluation import *
import math
import concurrent.futures
import time
from colorama import Fore, Style, init
init(convert=True)

class ChessAI:
    def __init__(self, maxDepth = 4, isWhite = False):
        self.maxDepth = maxDepth
        self.isWhite = isWhite
        for _ in range(3):
            print("")
        print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}AI:{Fore.WHITE} Hello there...")
 
    def play(self, board):
        print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}AI:{Fore.WHITE} I am thinking... {Fore.LIGHTMAGENTA_EX}Depth: {Fore.WHITE}{self.maxDepth}")
        start = time.perf_counter()
        nextMove, evaluation, totalLeafs = self.findBestMove(board, -math.inf, math.inf)
        end = time.perf_counter()
        aiMessage = f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}AI: {Fore.WHITE}"
        if nextMove:
            aiMessage += f"I found a move! "
            aiMessage += f"{Fore.RED}Eval:{Fore.WHITE} {round(evaluation, 2)}, "
            aiMessage += f"{Fore.YELLOW}Leafs:{Fore.WHITE} {totalLeafs}, "
            aiMessage += f"{Fore.GREEN}Time:{Fore.WHITE} {round(end-start, 2)}s"
        else:
            nextMove = (-69, -69)
            aiMessage += f"I resign! Well played. "
            aiMessage += f"{Fore.RED}Eval:{Fore.WHITE} {round(evaluation, 2)}, "
            aiMessage += f"{Fore.YELLOW}Leafs:{Fore.WHITE} {totalLeafs}, "
            aiMessage += f"{Fore.GREEN}Time:{Fore.WHITE} {round(end-start, 2)}s"
        print(aiMessage)
        return nextMove

    def findBestMove(self, board, alpha, beta):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            possibleMoves = []
            for move in board.moves:
                action = board.move(move[0], move[1])
                if action >= 0:
                    possibleMoves.append(move)
                    board.takeBack()
            if len(possibleMoves) > 1:
                branches = []
                for move in possibleMoves:
                    boardCopy = ChessBoard(board)
                    boardCopy.move(move[0], move[1])
                    f = executor.submit(self.minimax, boardCopy, alpha, beta, not self.isWhite, 1)
                    branches.append( (move, f) )
                chosenMove = None; chosenScore = -math.inf if self.isWhite else math.inf
                totalLeafs = 0
                print(f"{len(branches)} processes started")
                for branch in branches:
                    _, score, leafs = branch[1].result()
                    totalLeafs += leafs
                    if self.isWhite: # maximizing
                        if score > chosenScore: # max()
                            chosenScore = score
                            chosenMove = branch[0]
                    else:
                        if score < chosenScore: # min()
                            chosenScore = score
                            chosenMove = branch[0]
                return (chosenMove, chosenScore, totalLeafs)
            elif len(possibleMoves) == 1:
                return (possibleMoves[0], 0, 1)
            else:
                return (None, 0, 0)

    def minimax(self, board, alpha, beta, maximizingPlayer, currentDepth):
        if (currentDepth == self.maxDepth):
            return (None, evaluate(board), 1) # return score and one leaf
        if maximizingPlayer:
            bestMove = None; bestScore = -math.inf
            totalLeafs = 0
            for move in board.moves:
                action = board.move(move[0], move[1])
                if action >= 0: # move isn't illegal?
                    # throw away move, only score needed
                    _, score, leafs = self.minimax(board, alpha, beta, False, currentDepth + 1)
                    totalLeafs += leafs
                    board.takeBack() # only has to be done if not illegal
                    if score > bestScore: # max()
                        bestScore = score
                        bestMove = move
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            if not bestMove:
                if board.standsCheck(maximizingPlayer):
                    bestScore = 0 # prevent stalemate??
            return (bestMove, bestScore, totalLeafs)
        else:
            worstMove = None; worstScore = math.inf
            totalLeafs = 0
            for move in board.moves:
                action = board.move(move[0], move[1])
                if action >= 0: # move illegal
                    # throw away move, only score needed
                    _, score, leafs = self.minimax(board, alpha, beta, True, currentDepth + 1)
                    totalLeafs += leafs
                    board.takeBack()
                    if score < worstScore: # min()
                        worstScore = score
                        worstMove = move
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            if not worstMove:
                if board.standsCheck(not maximizingPlayer):
                    worstScore = 0 # prevent stalemate
            return (worstMove, worstScore, totalLeafs)
