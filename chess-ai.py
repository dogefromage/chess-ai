
import pygame
pygame.init()
screen = pygame.display.set_mode((600, 700), pygame.RESIZABLE)
pygame.display.set_caption("Chess AI")

from ChessBoard import ChessBoard
board = ChessBoard()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            board.click(event.pos)

    screen.fill((50, 50, 50))
    board.draw(screen)
    
    pygame.display.update()
