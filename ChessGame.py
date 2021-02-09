

class ChessGame:

pieces = {
    11: Rook(pygame.image.load('pieces/rook-white.png'), False),
    12: Knight(pygame.image.load('pieces/knight-white.png'), False),
    13: Bishop(pygame.image.load('pieces/bishop-white.png'), False),
    14: Queen(pygame.image.load('pieces/queen-white.png'), False),
    10: King(pygame.image.load('pieces/king-white.png'), False),
    1: Pawn(pygame.image.load('pieces/pawn-white.png'), False),
    21: Rook(pygame.image.load('pieces/rook-black.png'), True),
    22: Knight(pygame.image.load('pieces/knight-black.png'), True),
    23: Bishop(pygame.image.load('pieces/bishop-black.png'), True),
    24: Queen(pygame.image.load('pieces/queen-black.png'), True),
    20: King(pygame.image.load('pieces/king-black.png'), True),
    2: Pawn(pygame.image.load('pieces/pawn-black.png'), True),
}

def recalculateCamera(self):
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



    recalculateCamera(screen)
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
    