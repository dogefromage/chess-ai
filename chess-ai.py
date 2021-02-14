if __name__ == "__main__":
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 800), pygame.RESIZABLE)
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
                if event.key == pygame.K_o:
                    game.overlay = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    game.overlay = False

        screen.fill((50, 50, 50))
        game.draw(screen)
        pygame.display.update()
        if not game.gameOver:
            game.aiPlay()