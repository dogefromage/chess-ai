import pygame

class Piece:
    def __init__(self, img, isBlack, value):
        self.img = img
        self.isBlack = isBlack
        self.value = value

class Knight(Piece):
    def __init__(self, img, isBlack):
        Piece.__init__(self, img, isBlack, 3)
        self.moveStyle = 'absolute'
        self.moves = [
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
            (2, 1)
        ]

class Pawn(Piece): # cuck
    def __init__(self, img, isBlack):
        Piece.__init__(self, img, isBlack, 1)
        self.moveStyle = 'pawn' 
        self.moves = [
            (1, 1),
            (-1, 1),
            (0, 1),
            (0, 2),
        ]

class Queen(Piece):
    def __init__(self, img, isBlack):
        Piece.__init__(self, img, isBlack, 9)
        self.moveStyle = 'continuous'
        self.moves = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1)
        ]  

class King(Piece):
    def __init__(self, img, isBlack): 
        Piece.__init__(self, img, isBlack, 10) # value???
        self.moveStyle = 'absolute'
        self.moves = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1)
        ]

class Rook(Piece):
    def __init__(self, img, isBlack):
        Piece.__init__(self, img, isBlack, 5)
        self.moveStyle = 'continuous'
        self.moves = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        ]  

class Bishop(Piece):
    def __init__(self, img, isBlack):
        Piece.__init__(self, img, isBlack, 3)
        self.moveStyle = 'continuous'
        self.moves = [
            (1, 1),
            (-1, 1),
            (-1, -1),
            (1, -1)
        ]  

pieces = {
    "RW": Rook(pygame.image.load('pieces/rook-white.png'), False),
    "NW": Knight(pygame.image.load('pieces/knight-white.png'), False),
    "BW": Bishop(pygame.image.load('pieces/bishop-white.png'), False),
    "QW": Queen(pygame.image.load('pieces/queen-white.png'), False),
    "KW": King(pygame.image.load('pieces/king-white.png'), False),
    "-W": Pawn(pygame.image.load('pieces/pawn-white.png'), False),
    "RB": Rook(pygame.image.load('pieces/rook-black.png'), True),
    "NB": Knight(pygame.image.load('pieces/knight-black.png'), True),
    "BB": Bishop(pygame.image.load('pieces/bishop-black.png'), True),
    "QB": Queen(pygame.image.load('pieces/queen-black.png'), True),
    "KB": King(pygame.image.load('pieces/king-black.png'), True),
    "-B": Pawn(pygame.image.load('pieces/pawn-black.png'), True),
}
