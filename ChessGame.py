from multiprocessing import Manager, managers
from ChessBoard import ChessBoard
import pygame
from pygame.locals import *
from ChessAI import ChessAI

pieceImagePaths = {
    (11, 'pieces/rook-white.png'),
    (12, 'pieces/knight-white.png'),
    (13, 'pieces/bishop-white.png'),
    (14, 'pieces/queen-white.png'),
    (10, 'pieces/king-white.png'),
    (1,  'pieces/pawn-white.png'),
    (21, 'pieces/rook-black.png'),
    (22, 'pieces/knight-black.png'),
    (23, 'pieces/bishop-black.png'),
    (24, 'pieces/queen-black.png'),
    (20, 'pieces/king-black.png'),
    (2,  'pieces/pawn-black.png')
}

pieces = {}
for key, link in pieceImagePaths:
    pieces[key] = pygame.image.load(link)

class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.selection = 0
        self.available = []
        self.lastPlayed = ()
        self.gameInfo = "White to move"
        self.gameOver = False
        self.AI = ChessAI()
        self.overlay = False
    
    def recalculateCamera(self, screen):
        W, H = screen.get_size()
        w = W - 50; h = H - 50 # margin
        self.scale = int(min(w, h) / 8)
        self.left = (W - self.scale * 8) * 0.5
        self.top = (H - self.scale * 8) * 0.5

    def BoardToScreen(self, index):
        i = index % 10 - 1
        j = index // 10 - 2
        x = int(self.left + self.scale * i)
        y = int(self.top + self.scale * j)
        return (x, y)

    def ScreenToBoard(self, coords):
        x, y = coords
        i = int((x - self.left) / self.scale)
        j = int((y - self.top) / self.scale)
        return i + 10 * j + 21 # account for 1D board with margins

    def aiPlay(self):
        if self.board.whitesTurn == self.AI.isWhite:
            move = self.AI.play(self.board)
            if move == (-69, -69):
                self.gameInfo = "AI resigns!"
                self.gameOver = True
            else:
                self.select(move[0])
                self.select(move[1])

    def draw(self, screen):
        self.recalculateCamera(screen)
        for index in range(len(self.board.board)):
            if self.board.board[index] < 0:
                continue # skip margin squares when drawing
            screenCoords = self.BoardToScreen(index)
            rect = Rect(screenCoords, (self.scale, self.scale))
            # square color
            darkField = (index - index // 10) % 2 == 0 # ?? but works
            selectedField = self.selection == index
            availableField = False
            for a in self.available:
                if (a == index):
                    availableField = True; break
            justPlayedField = False
            for f in self.lastPlayed:
                if index == f:
                    justPlayedField = True
            color = "#ff00ff"
            if availableField or selectedField:
                color = "#9aedb5" if darkField else "#4ea36d"
            elif justPlayedField:
                color = "#f4e992" if darkField else "#ddce5d"
            else:
                color = "#edd09a" if darkField else "#a3854e"

            pygame.draw.rect(screen, color, rect)
            # piece
            piece = pieces.get(self.board.board[index])
            if piece:
                screen.blit(pygame.transform.scale(piece, (self.scale, self.scale)), screenCoords)
            
            # number overlay
            if self.overlay:
                font = pygame.font.SysFont(None, 30)
                img = font.render(f"{index}", True, "#ff0000")
                screen.blit(img, screenCoords)
        font = pygame.font.SysFont(None, 60)
        img = font.render(self.gameInfo, True, "#dddddd")
        screen.blit(img, (20, 20))

    def click(self, coords):
        self.select(self.ScreenToBoard(coords))

    def select(self, index):
        for a in self.available:
            if a == index:
                result = self.board.move(self.selection, a)
                if result >= 0:
                    self.lastPlayed = (self.selection, a)
                    self.gameInfo, self.gameOver = self.board.getGameState()
                self.selection = 0; self.available = []
                return
        self.selection = index
        self.available = self.board.getAvailable(index)

    def takeBack(self):
        self.board.takeBack()
        self.board.takeBack()
        self.selection = 0; self.available = []