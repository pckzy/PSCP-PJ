"""PROJECT PSCP"""
# use pygame to create
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 1010
screen = pygame.display.set_mode([WIDTH, HEIGHT])
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
tickrate = 50
timer = pygame.time.Clock()

run = True
while run:
    screen.fill('black') # change soon to picture
    timer.tick(tickrate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit game
            run = False
    pygame.display.flip()
pygame.quit()
