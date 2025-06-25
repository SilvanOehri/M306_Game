import pygame
import sys
import config
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Beercatcher")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = Game()

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()

        game.update(keys)
        game.draw(screen, font)
        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()