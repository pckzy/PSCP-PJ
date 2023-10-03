"""PROJECT PSCP"""
# use pygame to create
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 800 # 800notebook , 1010pc
screen = pygame.display.set_mode([WIDTH, HEIGHT])
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption('Survive from typing')
tickrate = 50
timer = pygame.time.Clock()

header_font = pygame.font.Font('resources/fonts/Square.ttf', 50)
name_font = pygame.font.Font('resources/fonts/Square.ttf', 31)

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

def draw_screen():
    pygame.draw.rect(screen, 'black', [0, HEIGHT - 100, WIDTH, 100], 0) #UNDER (32, 42, 68)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, 40], 0)
    pygame.draw.line(screen, 'white', (1200, 43), (0, 43), 5) #UNDER TOP
    pygame.draw.line(screen, 'white', (255, HEIGHT - 100), (255, HEIGHT), 2) #SEP UNDER LEFT
    pygame.draw.line(screen, 'white', (720, HEIGHT - 100), (720, HEIGHT), 2) #SEP UNDER RIGHT
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 5) #TOP UNDER
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 3)

run = True
while run:
    screen.fill('cornsilk4') # change soon to picture
    timer.tick(tickrate)
    draw_screen()
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit game
            run = False
    pygame.display.flip()
pygame.quit()
