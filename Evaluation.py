def evaluate(board):
    score = 0
    # piece balance
    for square in board.board:
        if square > 0:
            score += pieceValues[square]
    # 0.1 * possible move count
    if board.whitesTurn:
        score += 0.1 * len(board.moves)
        othersMoves = board.generateMoves(False)
        score -= 0.1 * len(othersMoves)
    else:
        score -= 0.1 * len(board.moves)
        othersMoves = board.generateMoves(False)
        score += 0.1 * len(othersMoves)
    return score

pieceValues = {
    1: 1,
    10: 200,
    11: 5,
    12: 3,
    13: 3,
    14: 9,
    2: -1,
    20: -200,
    21: -5,
    22: -3,
    23: -3,
    24: -9,
}