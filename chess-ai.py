
import pygame
pygame.init()
screen = pygame.display.set_mode((600, 700), pygame.RESIZABLE)
pygame.display.set_caption("Chess AI")

from ChessGame import ChessGame
game = ChessGame()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.takeBack()

    screen.fill((50, 50, 50))
    game.draw(screen)
    pygame.display.update()