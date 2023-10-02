"""PROJECT PSCP"""
# use pygame to create
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 1010
screen = pygame.display.set_mode([WIDTH, HEIGHT])
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
tickrate = 50
timer = pygame.time.Clock()

def draw_menu():
    """main menu tabs"""
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # LEFT SIDE
    pygame.draw.rect(surface, (0, 0, 0, 100), [70, 80, 600, 750], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [70, 80, 600, 750], 5, 5)

    # RIGHT SIDE
    pygame.draw.rect(surface, (0, 0, 0, 100), [720, 80, 400, 750], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [720, 80, 400, 750], 5, 5)

    screen.blit(surface, (0, 0))

run = True
while run:
    screen.fill('cornsilk4') # change soon to picture
    timer.tick(tickrate)
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit game
            run = False
    pygame.display.flip()
pygame.quit()
