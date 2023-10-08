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

# game resources
background = pygame.image.load("resources/images/projectbg.png")
header_font = pygame.font.Font("resources/fonts/Square.ttf", 50)
name_font = pygame.font.Font("resources/fonts/Square.ttf", 31)
banner_font = pygame.font.Font("resources/fonts/1up.ttf", 28)
mc_font = pygame.font.Font("resources/fonts/Minecrafter.Reg.ttf", 40)
pause_font = pygame.font.Font('resources/fonts/1up.ttf', 38)

# game variable
score = 0
high_score = 0 # use file.open soon
total_type = 0
lives = 5 # default = 5
level = 1
active_string = ""
paused = True

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        btn_shape = pygame.draw.circle(self.surf, (0, 0, 0), (self.x_pos, self.y_pos), 35)
        if btn_shape.collidepoint(pygame.mouse.get_pos()):
            btn_event = pygame.mouse.get_pressed()
            if btn_event[0]: # HOLD AND CLICK
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35) # click
                self.clicked = True
            else: # HOLD BUT NOT CLICK
                pygame.draw.circle(self.surf, (121, 120, 120), (self.x_pos, self.y_pos), 35) # hold
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))

def draw_menu():
    """main menu tabs"""
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # LEFT SIDE
    pygame.draw.rect(surface, (0, 0, 0, 50), [70, 70, 600, 590], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [70, 70, 600, 590], 5, 5)
    surface.blit(header_font.render('MENU :', True, 'black'), (95, 90))
    btn_resume = Button(125, 190, '>', False, surface)
    surface.blit(header_font.render('PLAY!', True, 'white'), (175, 165))
    btn_quit = Button(375, 190, 'X', False, surface)
    surface.blit(header_font.render('QUIT!', True, 'white'), (425, 165))
    btn_resume.draw()
    btn_quit.draw()

    # RIGHT SIDE
    pygame.draw.rect(surface, (0, 0, 0, 50), [720, 70, 400, 590], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [720, 70, 400, 590], 5, 5)

    screen.blit(surface, (0, 0))
    return btn_resume.clicked, btn_quit.clicked

def draw_screen():
    # screen border
    pygame.draw.rect(screen, 'black', [0, HEIGHT - 100, WIDTH, 100], 0) #UNDER (32, 42, 68)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, 40], 0)
    pygame.draw.line(screen, 'white', (1200, 42), (0, 42), 5) #UNDER TOP
    pygame.draw.line(screen, 'white', (255, HEIGHT - 100), (255, HEIGHT), 2) #SEP UNDER LEFT
    pygame.draw.line(screen, 'white', (720, HEIGHT - 100), (720, HEIGHT), 2) #SEP UNDER RIGHT
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 5) #TOP UNDER
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 3)

    # screen text
    screen.blit(banner_font.render(f'SCORE: {score}', True, 'white'), (240, 1))
    screen.blit(banner_font.render(f'BEST: {high_score}', True, 'white'), (550, 1))
    screen.blit(banner_font.render(f'TOTAL WORD: {total_type}', True, 'white'), (835, 1))
    screen.blit(banner_font.render(f'LIVES: {lives}', True, 'white'), (12, 1))
    screen.blit(mc_font.render(f'Level: {level}', True, 'white'), (15, HEIGHT - 67))
    screen.blit(header_font.render(f'"{active_string}"', True, 'white'), (280, HEIGHT - 75))
    screen.blit(mc_font.render(f'PSCP-PROJECT', True, 'white'), (845, HEIGHT - 67))

    # button
    pause_btn = Button(778, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    return pause_btn.clicked

run = True
while run:
    screen.blit(background, (0, 0))
    timer.tick(tickrate)
    stop_btn = draw_screen()
    if paused == True:
        draw_menu()
        resume_btn, quit_btn = draw_menu()
        if resume_btn:
            paused = False
        if quit_btn:
            run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit game
            run = False
    if stop_btn:
        paused = True
    pygame.display.flip()
pygame.quit()
