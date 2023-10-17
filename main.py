"""PROJECT PSCP"""
# use pygame to create
import pygame, music, copy, random

pygame.init()

from nltk.corpus import words
wordlist = words.words()
len_indexes = []
list_ofword = []
lenght = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > lenght:
        lenght += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))

WIDTH, HEIGHT = 1400, 800 # 800notebook , 1010pc
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
game_font = pygame.font.Font('resources/fonts/JoeJack.ttf', 33)
on_img = pygame.image.load('resources/images/on.png').convert_alpha()
off_img = pygame.image.load('resources/images/off.png').convert_alpha()
addlife_img = pygame.image.load('resources/images/plus.png').convert_alpha()
minuslife_img = pygame.image.load('resources/images/minus.png').convert_alpha()

# game variable
score = 0
total_type = 0
lives = 4 # default = 5
level = 0
active_string = ""
submit = ""
paused = True
music_paused = False
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lenght_select = [True, False, False, False, False, False, False]
new_lvl = True
word_objects = []
scroll_offset = 0
item_height = 40
visible_items = 15
cheat = False

# game sound
pygame.mixer.init()
pygame.mixer.music.load('resources/sounds/music.mp3')
click = pygame.mixer.Sound('resources/sounds/click.mp3')
woosh = pygame.mixer.Sound('resources/sounds/Swoosh.mp3')
wrong = pygame.mixer.Sound('resources/sounds/Instrument Strum.mp3')
lose = pygame.mixer.Sound('resources/sounds/hurt.mp3')
lose_fx = pygame.mixer.Sound('resources/sounds/lose_fx.wav')
music_img = pygame.image.load('resources/images/music_logo.png').convert_alpha()
music_button = pygame.Rect(569, 155, 74, 72)
song_btn = music.btn(565, 150, music_img, 0.4)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
click.set_volume(0.3)
woosh.set_volume(0.1)
wrong.set_volume(0.3)
lose.set_volume(0.3)
lose_fx.set_volume(0.3)
cheat_button = pygame.Rect(1020, 410, 400, 65)
on_logo = music.btn(1237, 722, on_img, 0.4)
off_logo = music.btn(1237, 722, off_img, 0.4)
addlife_btn = music.btn(1020, 280, addlife_img, 0.4)
addlvl_btn = music.btn(1020, 220, addlife_img, 0.4)
add_box = pygame.Rect(1020, 280, 45, 45)
minuslife_btn = music.btn(770, 280, minuslife_img, 0.4)
minuslvl_btn = music.btn(770, 220, minuslife_img, 0.4)
minus_box = pygame.Rect(770, 280, 45, 45)
addlvl_box = pygame.Rect(1020, 220, 45, 45)
minuslvl_box = pygame.Rect(770, 220, 45, 45)
clear_box = pygame.Rect(770, 150, 300, 55)

file = open('high_score.txt', 'r')
read = file.readline()
high_score = int(read[:])
total_type = 0
file.close()

menuclr_box = pygame.Rect(945, 605, 400, 40)
txtclr_box = pygame.Rect(945, 555, 400, 40)
txt_color, txt_color_2 = "", ""
color_inactive, color_active = pygame.Color('black'), pygame.Color('grey')
color_inactive_2, color_active_2 = pygame.Color('black'), pygame.Color('grey')
menu_color, menu_color_diff, str_color = pygame.Color('black'), pygame.Color('white'), pygame.Color('white')
color, color_2 = color_inactive, color_inactive
active, active_2 = False, False

class Word:
    def __init__(self, text, speed, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed
    
    def draw(self): # game string green if correct
        color = ('black')
        screen.blit(game_font.render(self.text, True, color), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(game_font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))

    def update(self):
        x_speed = random.randint(-2, 2)
        self.y_pos += self.speed
        self.x_pos += x_speed

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
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3) # circle border
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))

def draw_menu():
    """main menu tabs"""
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    # LEFT SIDE
    pygame.draw.rect(surface, (0, 0, 0, 50), [70, 70, 600, 590], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [70, 70, 600, 590], 5, 5)
    song_btn.draw(surface)
    if not music_paused:
        pygame.draw.circle(surface, 'green', (605, 192), 40, 5)
    else:
        pygame.draw.circle(surface, 'red', (605, 191), 40, 3)
        pygame.draw.line(surface, 'red', (579, 220), (627, 161), 4)
    surface.blit(header_font.render('MENU :', True, 'black'), (95, 90))
    btn_resume = Button(125, 190, '>', False, surface)
    surface.blit(header_font.render('PLAY!', True, str_color), (175, 165))
    btn_quit = Button(375, 190, 'X', False, surface)
    surface.blit(header_font.render('QUIT!', True, str_color), (425, 165))
    btn_resume.draw()
    btn_quit.draw()

    # GAME LENGHT
    surface.blit(header_font.render('Active Letter Lengths:', True, 'black'), (95, 240))
    len_pick = copy.deepcopy(lenght_select)
    for i in range(len(lenght_select)):
        word_len = Button(125 + (i*80), 340, str(i+2), False, surface)
        word_len.draw()
        if word_len.clicked:
            if len_pick[i]:
                len_pick[i] = False
            else:
                len_pick[i] = True
        if lenght_select[i]:
            pygame.draw.circle(surface, 'green', (125 + (i*80), 340), 35, 5)
        else:
            pygame.draw.circle(surface, 'red', (125 + (i*80), 340), 35, 5)
            pygame.draw.line(surface, 'red', (103 + (i*80), 364), (143 + (i*80), 314), 5)

    # TEXT
    surface.blit(header_font.render('CREDIT :', True, 'black'), (95, 390))
    surface.blit(name_font.render('66070309 : SARUN MANPRAPHAN', True, str_color), (95, 450))
    surface.blit(name_font.render('66070195  : SUPHANUT NGAMGETSOOK', True, str_color), (95, 490))
    surface.blit(name_font.render('66070183  : Wathasin Huaihongtong', True, str_color), (95, 530))
    surface.blit(name_font.render('66070247 : Chanokchon Pancome', True, str_color), (95, 570))
    surface.blit(name_font.render('66070239 : Kittiphot Mongkolrat', True, str_color), (95, 610))

    # RIGHT SIDE
    pygame.draw.rect(surface, (0, 0, 0, 50), [720, 70, 400, 590], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [720, 70, 400, 590], 5, 5)

    surface.blit(header_font.render('CHEAT :', True, 'black'), (740, 90))
    surface.blit(name_font.render('Add level', True, str_color), (843, 230))
    surface.blit(name_font.render('Add life', True, str_color), (855, 290))
    surface.blit(header_font.render('GAME HELPER :', True, 'black'), (740, 347))
    surface.blit(name_font.render('SHOW WORD LIST :', True, str_color), (740, 425))
    btn_word = Button(1055, 440, 'Y', False, surface)
    btn_word.draw()
    if cheat:
        pygame.draw.circle(surface, 'green', (1055, 440), 37, 5)
    else:
        pygame.draw.circle(surface, 'red', (1055, 440), 37, 5)
        pygame.draw.line(surface, 'red', (1034, 467), (1075, 413), 5)
    surface.blit(header_font.render('COLOR SETTING :', True, 'black'), (740, 490))
    surface.blit(name_font.render('TEXT COLOR :', True, str_color), (740, 560))
    surface.blit(name_font.render('TABS COLOR :', True, str_color), (740, 610))
    addlife_btn.draw(surface)
    minuslife_btn.draw(surface)
    addlvl_btn.draw(surface)
    minuslvl_btn.draw(surface)
    pygame.draw.rect(surface, 'black', (770, 150, 300, 55), 0, 5)
    surface.blit(header_font.render('CLEAR WORD', True, str_color), (782, 153))

    screen.blit(surface, (0, 0))
    return btn_resume.clicked, btn_quit.clicked, len_pick

def draw_screen():
    # screen border
    pygame.draw.rect(screen, menu_color, [0, HEIGHT - 100, WIDTH, 100], 0) #UNDER (32, 42, 68)
    pygame.draw.rect(screen, menu_color, [0, 0, WIDTH, 40], 0)
    pygame.draw.line(screen, menu_color_diff, (1200, 42), (0, 42), 5) #UNDER TOP
    pygame.draw.line(screen, menu_color_diff, (255, HEIGHT - 100), (255, HEIGHT), 5) #SEP UNDER LEFT
    pygame.draw.line(screen, menu_color_diff, (720, HEIGHT - 100), (720, HEIGHT), 5) #SEP UNDER RIGHT
    pygame.draw.line(screen, menu_color_diff, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 5) #TOP UNDER
    pygame.draw.rect(screen, menu_color, [0, 0, WIDTH, HEIGHT], 3)

    # screen text
    screen.blit(banner_font.render(f'SCORE: {score}', True, str_color), (240, 1))
    screen.blit(banner_font.render(f'BEST: {high_score}', True, str_color), (550, 1))
    screen.blit(banner_font.render(f'TOTAL WORD: {total_type}', True, str_color), (835, 1))
    screen.blit(banner_font.render(f'LIVES: {lives}', True, str_color), (12, 1))
    screen.blit(mc_font.render(f'Level: {level}', True, str_color), (15, HEIGHT - 67))
    screen.blit(header_font.render(f'"{active_string}"', True, str_color), (280, HEIGHT - 75))
    screen.blit(mc_font.render(f'PSCP-PROJECT', True, str_color), (845, HEIGHT - 67))

    # button
    pause_btn = Button(778, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    return pause_btn.clicked

def check_highscore():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

def generate_level():
    word_object = []
    include = []
    item_list = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in lenght_select: # if all false = unplayable
        lenght_select[0] = True
    for i in range(len(lenght_select)):
        if lenght_select[i]:
            include.append((len_indexes[i], len_indexes[i+1]))
    for i in range(level):
        speed = random.randint(1, 3)
        y_pos = random.randint(-265, -5)
        x_pos = random.randint(10 + (i * vertical_spacing), (i+1) * vertical_spacing)
        index_selection = random.choice(include) # random text
        index = random.randint(index_selection[0], index_selection[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, x_pos, y_pos)
        word_object.append(new_word)
        item_list.append(text)
    return word_object, item_list

def check_score(point):
    for word in word_objects:
        if word.text == submit:
            int_point = word.speed * len(word.text) * 7 * (len(word.text) / 3)
            point += int(int_point)
            word_objects.remove(word)
            woosh.play()
    return point

def game_helper():
    if submit in list_ofword:
        list_ofword.remove(submit)
    pygame.draw.rect(screen, menu_color, [1200, 0, 1400, 800], 0)
    pygame.draw.line(screen, menu_color_diff, (1200, 0), (1200, 796), 5)
    pygame.draw.line(screen, menu_color_diff, (1200, 70), (1400, 70), 5)
    pygame.draw.line(screen, menu_color_diff, (1200, 700), (1400, 700), 5)
    screen.blit(header_font.render('word', True, str_color), (1240, 10))
    on_logo.draw(screen)
    if len(list_ofword) >= 1:
        start_item = max(0, len(list_ofword) - visible_items - scroll_offset)
        end_item = min(len(list_ofword) - scroll_offset, len(list_ofword))
        for i, item in enumerate(list_ofword[start_item:end_item]):
            item_text = name_font.render(item, True, str_color)
            screen.blit(item_text, (1298 - len(str(item))*9, 90 + i * item_height))

run = True
while run:
    screen.blit(background, (0, 0))
    timer.tick(tickrate)
    # x, y = pygame.mouse.get_pos()
    # print(x, y)
    if new_lvl and not paused:
        word_objects, list_ofword = generate_level()
        new_lvl = False
    else:
        for words in word_objects:
            words.draw()
            if not paused:
                words.update()
            if words.y_pos > 700: # y pos that text gone
                word_objects.remove(words)
                lose.play()
                lives -= 1
    if paused == True:
        draw_menu()
        resume_btn, quit_btn, select = draw_menu()
        txt_surface, txt_surface_2 = name_font.render(txt_color, True, 'black'), name_font.render(txt_color_2, True, 'black')
        width, width_2 = max(155, txt_surface.get_width() + 10), max(155, txt_surface_2.get_width() + 10)
        menuclr_box.w, txtclr_box.w = width, width_2
        screen.blit(txt_surface, (menuclr_box.x + 5, menuclr_box.y + 5))
        screen.blit(txt_surface_2, (txtclr_box.x + 5, txtclr_box.y + 5))
        pygame.draw.rect(screen, color, menuclr_box, 4, 4)
        pygame.draw.rect(screen, color_2, txtclr_box, 4, 4)
        if resume_btn:
            paused = False
        if quit_btn:
            run = False
    if len(word_objects) <= 0 and not paused:
        level += 1
        lives += 1
        new_lvl = True
    if submit != '':
        init = score
        score = check_score(score)
        submit = ''
        if init == score:
            wrong.play()
            pass
        else:
            total_type += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # exit game
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if music_button.collidepoint(event.pos):
                music_paused = not music_paused
                if music_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if menuclr_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            if txtclr_box.collidepoint(event.pos):
                active_2 = not active_2
            else:
                active_2 = False
            color = color_active if active else color_inactive
            color_2 = color_active_2 if active_2 else color_inactive_2
            if cheat_button.collidepoint(event.pos):
                cheat = not cheat
                woosh.play()
            if add_box.collidepoint(event.pos):
                lives += 1
            if minus_box.collidepoint(event.pos):
                lives -= 1
            if addlvl_box.collidepoint(event.pos):
                level += 1
            if minuslvl_box.collidepoint(event.pos):
                level -= 1
            if clear_box.collidepoint(event.pos):
                word_objects.clear()
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                    click.play()
                if event.key == pygame.K_BACKSPACE and pygame.key.get_mods() & pygame.KMOD_CTRL \
                    or event.key == pygame.K_BACKSPACE and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    active_string = ""
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0: #DEL INPUT TEXT
                    active_string = active_string[:-1]
                    click.play()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
                if event.key == pygame.K_SLASH:
                    cheat = not cheat
                    woosh.play()
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True
            if active and paused:
                if event.key == pygame.K_RETURN:
                    try:
                        if txt_color == 'white':
                            menu_color_diff = pygame.Color('black')
                        elif txt_color == 'black':
                            menu_color_diff = pygame.Color('white')
                        menu_color = pygame.Color(txt_color)
                    except ValueError:
                        wrong.play()
                    txt_color = ""
                elif event.key == pygame.K_BACKSPACE:
                    txt_color = txt_color[:-1]
                else:
                    txt_color += event.unicode
            if active_2 and paused:
                if event.key == pygame.K_RETURN:
                    try:
                        str_color = pygame.Color(txt_color_2)
                    except ValueError:
                        wrong.play()
                    txt_color_2 = ""
                elif event.key == pygame.K_BACKSPACE:
                    txt_color_2 = txt_color_2[:-1]
                else:
                    txt_color_2 += event.unicode
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                lenght_select = select
    stop_btn = draw_screen()
    if stop_btn:
        paused = True
    if score > high_score:
        check_highscore()
    if lives <= 0:
        paused = True
        lose_fx.play()
        level = 0
        lives = 4
        word_objects = []
        new_level = True
        check_highscore()
        score = 0
    if cheat:
        game_helper()
    else:
        pygame.draw.rect(screen, menu_color, [1203, 0, 1400, 800], 0)
        screen.blit(header_font.render('word', True, str_color), (1240, 10))
        pygame.draw.line(screen, menu_color_diff, (1200, 70), (1400, 70), 5)
        pygame.draw.line(screen, menu_color_diff, (1200, 0), (1200, 796), 5)
        pygame.draw.line(screen, menu_color_diff, (1200, 700), (1400, 700), 5)
        off_logo.draw(screen)
    pygame.display.flip()
pygame.quit()
