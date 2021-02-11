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
        self.gameState = "White to move"
        self.AI = ChessAI()
    
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

    def draw(self, screen):
        self.recalculateCamera(screen)
        for index in range(len(self.board.board)):
            if self.board.board[index] < 0:
                continue # skip margin squares when drawing
            screenCoords = self.BoardToScreen(index)
            rect = Rect(screenCoords, (self.scale, self.scale))
            # square color
            evenField = (index - index // 10) % 2 == 0 # ?? but works
            selectedField = self.selection == index
            availableField = False
            for a in self.available:
                if (a == index):
                    availableField = True; break
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
            pygame.draw.rect(screen, color, rect)
            # piece
            piece = pieces.get(self.board.board[index])
            if piece:
                screen.blit(pygame.transform.scale(piece, (self.scale, self.scale)), screenCoords)

        font = pygame.font.SysFont(None, 50)
        img = font.render(self.gameState, True, "#aaaaaa")
        w, h = screen.get_size()
        screen.blit(img, (20, 20))

    def click(self, coords):
        self.select(self.ScreenToBoard(coords))

    def select(self, index):
        for a in self.available:
            if a == index:
                self.board.move(self.selection, a)
                self.selection = 0; self.available = []
                
                # self.gameState = self.board.getGameState()

                # COMPUTER
                computerMove = self.AI.play(self.board)
                if computerMove:
                    self.board.move(computerMove[0], computerMove[1])
                self.gameState = self.board.getGameState()
                return

        self.selection = index
        self.available = self.board.getAvailable(index)
        

    def takeBack(self):
        self.board.takeBack()
        self.selection = 0; self.available = []