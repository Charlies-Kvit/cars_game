# Импортируем нужные библиотеки
from random import randint, choice
import pygame
import os
import sys
import sqlite3

# Загружаем и объявляем все нужные переменные
pygame.init()
road = pygame.image.load('interface/road.png')
pygame.display.set_caption('Сars Game')
size = WIDTH, HEIGHT = road.get_size()
screen = pygame.display.set_mode(size)
hp = 3
cars_images = [file for file in os.listdir('interface/cars') if file[file.rfind('.'):] == ".png"]
cars_images_pixel = [file for file in os.listdir('interface/cars_pixel') if file[file.rfind('.'):] == ".png"]
y1 = 0
y2 = -HEIGHT

FPS = 120

# Дефолтные настройки
database = sqlite3.connect(r"./config/data_base.db3")
db_cursor = database.cursor()
db_cursor.execute("""CREATE TABLE IF NOT EXISTS custom_setting(
                    id INTEGER PRIMARY KEY,
                    keys TEXT,
                    mode TEXT);""")
database.commit()

default_keys = ['W', 'S', 'A', 'D']

if db_cursor.execute("""SELECT COUNT(*) FROM custom_setting""").fetchone()[0] != 0:
    custom_keys = db_cursor.execute("""SELECT keys FROM custom_setting WHERE id=1""").fetchone()[0].split()
    mode = db_cursor.execute("""SELECT mode FROM custom_setting WHERE id=1""").fetchone()[0]
else:
    custom_keys = default_keys
    mode = 'normal'
    db_cursor.execute("""INSERT INTO custom_setting(id, keys, mode)
                                        VALUES(?, ?, ?)""", (1, ' '.join(custom_keys), mode))
    database.commit()

# Загружаем фоновую музыку и звуки
died_sound = pygame.mixer.Sound(os.path.join("interface", "game_sounds", "died_sound.mp3"))
died_sound.set_volume(0.5)
sound1 = pygame.mixer.Sound('interface/cars/sounds/gudok.ogg')
sound1.set_volume(0.5)
boom_sound = pygame.mixer.Sound(os.path.join("interface", "game_sounds", "boom.mp3"))
boom_sound.set_volume(0.5)
pygame.mixer.music.load(os.path.join("interface/game_sounds/background-music.mp3"))
pygame.mixer.music.set_volume(0.5)

keys = {49: '1', 50: '2', 51: '3', 52: '4', 53: '5',
        54: '6', 55: '7', 56: '8', 57: '9', 48: '0',
        113: 'Q', 119: 'W', 101: 'E', 114: 'R', 116: 'T',
        121: 'Y', 117: 'U', 105: 'I', 111: 'O', 112: 'P',
        97: 'A', 115: 'S', 100: 'D', 102: 'F', 103: 'G',
        104: 'H', 106: 'J', 107: 'K', 108: 'L', 122: 'Z',
        120: 'X', 99: 'C', 118: 'V', 98: 'B', 110: 'N',
        109: 'M', 13: 'Enter', 32: 'Spacebar',
        1073742049: 'Shift', 1073742048: 'Ctrl',
        9: 'Tab', 1073742050: 'Alt', 1073741903: 'Right',
        1073741904: 'Left', 1073741906: 'Up',
        1073741905: 'Down'}

with open('config/logs.txt', 'a', encoding='utf-8') as w:
    w.write('-----------Новая сессия------------\n')


# Загружает изображение


def load_image(name, colorkey=None):
    fullname = os.path.join('interface', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Главное меню


def main_menu():
    main_menu_sprites = pygame.sprite.Group()

    start_game = MenuElement(538, 350, 'main_menu/start_game.png', main_menu_sprites)
    settings = MenuElement(538, 450, 'main_menu/settings.png', main_menu_sprites)
    quit_game = MenuElement(538, 555, 'main_menu/quit.png', main_menu_sprites)

    bg = load_image('main_menu/main_menu_bg.png')
    screen.blit(bg, (0, 0))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for el in main_menu_sprites:
            el.hover(mouse_pos)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                terminate()
            if start_game.rect.collidepoint(*mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main()
            if settings.rect.collidepoint(*mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    open_settings()
            if quit_game.rect.collidepoint(*mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
        main_menu_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class MenuElement(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.x = x
        self.y = y
        self.i = image
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.rect[2] // 2
        self.rect.y = self.y - self.rect[3] // 2

    def hover(self, mouse_pos):
        if self.rect.collidepoint(*mouse_pos):
            pygame.draw.rect(screen, (160, 160, 160), self.rect, 0)
        else:
            pygame.draw.rect(screen, (126, 109, 97), self.rect, 0)


# Настройки


class Settings:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.sound = MenuElement(200, 100, 'settings/general_btn.png', self.buttons)
        self.graphics = MenuElement(535, 100, 'settings/graphics_btn.png', self.buttons)
        self.controls = MenuElement(865, 100, 'settings/controls_btn.png', self.buttons)

        self.sound_settings()

    def sound_settings(self):
        bg = load_image('settings/general_bg.png')
        screen.blit(bg, (0, 0))
        font = pygame.font.SysFont('fonts/Unbounded-VariableFont_wght.ttf', 40)

        value = 0.5

        while True:
            screen.blit(bg, (0, 0))
            music_value = round(pygame.mixer.music.get_volume(), 1)
            sound_value = round(sound1.get_volume(), 1)
            mouse_pos = pygame.mouse.get_pos()
            text_value1 = font.render(f'{round(value, 1)}', True, 'white')
            text_rect = text_value1.get_rect()
            text_rect.center = (885, 258)
            screen.blit(text_value1, text_rect)

            text_value2 = font.render(f'{round(music_value, 1)}', True, 'white')
            text_rect1 = text_value2.get_rect()
            text_rect1.center = (885, 328)
            screen.blit(text_value2, text_rect1)

            text_value3 = font.render(f'{round(sound_value, 1)}', True, 'white')
            text_rect2 = text_value3.get_rect()
            text_rect2.center = (885, 400)
            screen.blit(text_value3, text_rect2)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()

                if self.graphics.rect.collidepoint(*mouse_pos) and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.graphics_settings()
                elif self.controls.rect.collidepoint(*mouse_pos) and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.controls_settings()

                if 38 <= mouse_pos[0] <= 1036 and 197 <= mouse_pos[1] <= 289:
                    if event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_UP and value < 0.9:
                        value += 0.1
                        pygame.mixer.music.set_volume(value)
                        died_sound.set_volume(value)
                        sound1.set_volume(value)
                        boom_sound.set_volume(value)

                    elif event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_DOWN and value >= 0:
                        value -= 0.1
                        pygame.mixer.music.set_volume(value)
                        died_sound.set_volume(value)
                        sound1.set_volume(value)
                        boom_sound.set_volume(value)

                if 38 <= mouse_pos[0] <= 1036 and 290 <= mouse_pos[1] <= 362:
                    if event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_UP and music_value < 1:
                        music_value += 0.1
                        pygame.mixer.music.set_volume(music_value)

                    elif event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_DOWN and music_value >= 0:
                        music_value -= 0.1
                        pygame.mixer.music.set_volume(music_value)

                if 38 <= mouse_pos[0] <= 1036 and 363 <= mouse_pos[1] <= 433:
                    if event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_UP and music_value < 1:
                        sound_value += 0.1
                        died_sound.set_volume(sound_value)
                        sound1.set_volume(sound_value)
                        boom_sound.set_volume(sound_value)

                    elif event.type == pygame.KEYDOWN and \
                            event.key == pygame.K_DOWN and music_value >= 0:
                        sound_value -= 0.1
                        died_sound.set_volume(sound_value)
                        sound1.set_volume(sound_value)
                        boom_sound.set_volume(sound_value)

            self.buttons.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def graphics_settings(self):
        global mode
        bg = load_image('settings/graphics_bg.png')
        screen.blit(bg, (0, 0))

        buttons = pygame.sprite.Group()
        left_arr = MenuElement(522, 219, 'settings/left.png', buttons)
        right_arr = MenuElement(880, 219, 'settings/right.png', buttons)
        font = pygame.font.SysFont('fonts/Unbounded-VariableFont_wght.ttf', 40)

        while True:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(bg, (0, 0))

            if mode == 'normal':
                text = font.render('Обычный', True, 'white')
            else:
                text = font.render('Пиксельный', True, 'white')

            text_rect = text.get_rect()
            text_rect.center = (700, 219)
            screen.blit(text, text_rect)

            for el in buttons:
                el.hover(mouse_pos)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()

                if self.sound.rect.collidepoint(*mouse_pos) and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.sound_settings()
                elif self.controls.rect.collidepoint(*mouse_pos) and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.controls_settings()

                if left_arr.rect.collidepoint(*mouse_pos) or \
                        right_arr.rect.collidepoint(*mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if mode == 'normal':
                            mode = 'pixel'
                        else:
                            mode = 'normal'
                        db_cursor.execute("""UPDATE custom_setting SET mode=? WHERE id=1;""", (mode,))
                        database.commit()

            self.buttons.draw(screen)
            buttons.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    def controls_settings(self):
        global custom_keys, default_keys, keys
        bg = load_image('settings/controls_bg.png')
        screen.blit(bg, (0, 0))
        font = pygame.font.SysFont('fonts/Unbounded-VariableFont_wght.ttf', 40)

        while True:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(bg, (0, 0))
            if custom_keys == default_keys:
                for i in range(4):
                    btn = font.render(default_keys[i], True, 'white')
                    btn_rect = btn.get_rect()
                    btn_rect.center = (885, 242 + i * 78)
                    screen.blit(btn, btn_rect)
            else:
                for i in range(4):
                    btn = font.render(custom_keys[i], True, 'white')
                    btn_rect = btn.get_rect()
                    btn_rect.center = (885, 242 + i * 78)
                    screen.blit(btn, btn_rect)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    terminate()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()

                if self.graphics.rect.collidepoint(*mouse_pos) and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.graphics_settings()
                elif self.sound.rect.collidepoint(*mouse_pos) and \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    self.sound_settings()

                if 400 <= mouse_pos[0] <= 975 and 206 <= mouse_pos[1] <= 274 \
                        and event.type == pygame.KEYDOWN:
                    if event.key in keys.keys() and \
                            keys[event.key] not in custom_keys:
                        custom_keys[0] = keys[event.key]
                        db_cursor.execute("""UPDATE custom_setting SET keys=? WHERE id=1;""", (' '.join(custom_keys),))
                        database.commit()

                if 400 <= mouse_pos[0] <= 975 and 278 <= mouse_pos[1] <= 355 \
                        and event.type == pygame.KEYDOWN:
                    if event.key in keys.keys() and \
                            keys[event.key] not in custom_keys:
                        custom_keys[1] = keys[event.key]
                        db_cursor.execute("""UPDATE custom_setting SET keys=? WHERE id=1;""", (' '.join(custom_keys),))
                        database.commit()

                if 400 <= mouse_pos[0] <= 975 and 360 <= mouse_pos[1] <= 436 \
                        and event.type == pygame.KEYDOWN:
                    if event.key in keys.keys() and \
                            keys[event.key] not in custom_keys:
                        custom_keys[2] = keys[event.key]
                        db_cursor.execute("""UPDATE custom_setting SET keys=? WHERE id=1;""", (' '.join(custom_keys),))
                        database.commit()

                if 400 <= mouse_pos[0] <= 975 and 442 <= mouse_pos[1] <= 516 \
                        and event.type == pygame.KEYDOWN:
                    if event.key in keys.keys() and \
                            keys[event.key] not in custom_keys:
                        custom_keys[3] = keys[event.key]
                        db_cursor.execute("""UPDATE custom_setting SET keys=? WHERE id=1;""", (' '.join(custom_keys),))
                        database.commit()

            self.buttons.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


def open_settings():
    Settings()


# Экран конца игры


def game_over():
    global WIDTH, HEIGHT, screen, died_sound, hero, kolvo_coins
    con = sqlite3.connect(r"./config/data_base.db3")
    cur = con.cursor()
    cur.execute(f"UPDATE Player_records SET number_of_points = '{kolvo_coins}'")
    con.commit()
    cur.close()
    pygame.mouse.set_visible(True)
    for sprite in cars_sprites.sprites():
        all_sprites.remove(sprite)
        cars_sprites.remove(sprite)
        if sprite in easter_sprite.sprites():
            easter_sprite.remove(sprite)
    coins_sprites.clear(screen, screen)
    pygame.mixer.music.stop()
    died_sound.play()
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("ВЫ ПОГИБЛИ!", True, "red")
    text_x = HEIGHT // 2 - text.get_height() // 2
    text_y = WIDTH // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, "red", (text_x - 10, text_y - 10,
                                     text_w + 20, text_h + 20), 1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                died_sound.stop()
                main_menu()
        pygame.display.flip()


# Анимация дороги


def update_background():
    global y1, y2
    screen.blit(road, (0, y1))
    screen.blit(road, (0, y2))
    y1 += 5
    y2 += 5
    if y1 > HEIGHT:
        y1 = -HEIGHT
    if y2 > HEIGHT:
        y2 = -HEIGHT


# Создает на пути машинки и монеты


def random_appearence(over_cars, ccc=False):
    global easter_flag
    over_cars_cords = []
    for i in over_cars:
        over_cars_cords.append((i.rect.topleft[0], i.rect.topright[0]))
    # thirst, second, third = range(0, 233), range(234, 466), range(467, 700)
    asd = 0
    flag = True
    while flag:
        x = randint(100, WIDTH - 229)
        asd += 1
        with open('config/logs.txt', 'a') as w:
            w.write(str(x) + ' ' + str(asd) + '\n')
        kol_vo_sovp = 0
        for i in over_cars_cords:
            if x not in range(i[0], i[1] + 1) and x + 120 not in range(i[0], i[1] + 1):
                kol_vo_sovp += 1
        if kol_vo_sovp == len(over_cars_cords):
            if randint(1, 100) == 50 and easter_flag:
                EasterCar((x, -300), all_sprites, cars_sprites, easter_sprite)
                easter_flag, flag = False, False
                continue
            if ccc:
                Coin((x, -300), all_sprites, coins_sprites)
            else:
                if randint(1, 6) == 4:
                    Gruzovik((x, -500), all_sprites, cars_sprites)
                else:
                    Car((x, -300), all_sprites, cars_sprites)
            flag = False
            break
        else:
            kol_vo_sovp = 0


# Убивает все процессы напрочь


def terminate():
    try:
        con = sqlite3.connect(r"./config/data_base.db3")
        cur = con.cursor()
        cur.execute(f"UPDATE Player_records SET number_of_points = '{kolvo_coins}'")
        con.commit()
        cur.close()
    finally:
        with open("config/logs.txt", "w"):
            pass
        pygame.quit()
        sys.exit()


class HitPoints(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        self.image = load_image('heart.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = position[0]
        self.rect.centery = position[1]


# Работает как крестик - нажал на него - закрыл окно


class Xcross(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((2 * 10, 2 * 10),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 15
        self.rect.centery = 55

    def update(self, flag=False):
        global cursor
        if pygame.sprite.collide_mask(self, cursor) and flag:
            terminate()


# Самый главный спрайт - спрайт игрока


class Hero(pygame.sprite.Sprite):
    if mode == 'normal':
        image = load_image('hero_car.png')
    else:
        image = load_image('hero_car_pixel.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.U = 8
        self.rect.centerx = WIDTH / 2 - 15
        self.rect.centery = HEIGHT / 4 * 3 - 15

    def update(self):
        global UP, DOWN, RIGHT, LEFT, running, hp
        # Смотрим, врезался ли герой в какую-нибудь машинку
        for auto_car in cars_sprites.sprites():
            if pygame.sprite.collide_mask(self, auto_car):
                if auto_car in easter_sprite:
                    from easter_game import start_easter_egg
                    pygame.quit()
                    pygame.init()
                    start_easter_egg()
                    sys.exit()
                hp -= 1
                all_sprites.remove(hp_sprites.sprites()[-1])
                hp_sprites.remove(hp_sprites.sprites()[-1])
                all_sprites.remove(auto_car)
                cars_sprites.remove(auto_car)
                boom_sound.play()
                random_appearence(cars_sprites)
                if hp == 0:
                    running = False
                    game_over()
                # terminate()
        # Иначе смотрим, куда поедет наш спрайт
        if UP and self.rect.y > 0:
            self.rect = self.rect.move(0, -self.U)
        if DOWN and self.rect.y < HEIGHT - self.image.get_height():
            self.rect = self.rect.move(0, self.U)
        if LEFT and self.rect.x > 101:
            self.rect = self.rect.move(-self.U, 0)
        if RIGHT and self.rect.x < WIDTH - self.image.get_width() - 101:
            self.rect = self.rect.move(self.U, 0)

    def restart_hero(self):
        if mode == 'normal':
            image = load_image('hero_car.png')
        else:
            image = load_image('hero_car_pixel.png')

        self.image = image
        self.rect.centerx = WIDTH / 2 - 15
        self.rect.centery = HEIGHT / 4 * 3 - 15


# Спрайт машинок, которые появляются на пути


class Car(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        if mode == 'normal':
            self.image = load_image(os.path.join('cars', choice(cars_images)))
        else:
            self.image = load_image(os.path.join('cars_pixel', choice(cars_images_pixel)))

        self.U = randint(7, 12)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        # Если машинка выезжает за пределы дороги - толкаем ее обратно
        for auto_car in cars_sprites.sprites():
            if pygame.sprite.collide_mask(self, auto_car) and auto_car != self:
                self.U = 5
        xu = 0
        if self.rect.x < 101:
            xu = 2
        elif self.rect.x > WIDTH - self.image.get_width() - 101:
            xu = -2
        self.rect = self.rect.move(xu, self.U)


# Спрайт грузовика - в основном, как машинка, только с гудком и большой скоростью 


class Gruzovik(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        self.coin_flag = True
        if mode == 'normal':
            self.image = load_image(os.path.join('cars', 'special', 'gruz.png'))
        else:
            self.image = load_image(os.path.join('cars_pixel', 'special', 'gruz.png'))
        self.image = load_image(os.path.join('cars', 'special', 'gruz.png'))
        self.U = randint(13, 20)
        sound1.play()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        xu = 0
        if self.rect.x < 101:
            xu = 2
        elif self.rect.x > WIDTH - self.image.get_width() - 101:
            xu = -2
        self.rect = self.rect.move(xu, self.U)


# Те самые монетки)


class Coin(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        self.coin_flag = True
        if mode == 'normal':
            self.image = load_image('coin.png')
        else:
            self.image = load_image('coin_pixel.png')
        self.U = 5
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        global kolvo_coins, hero

        if mode == 'normal':
            self.image = load_image('coin.png')
        else:
            self.image = load_image('coin_pixel.png')

        xu = 0
        if self.rect.x < 101:
            xu = 2
        elif self.rect.x > WIDTH - self.image.get_width() - 101:
            xu = -2
        self.rect = self.rect.move(xu, self.U)
        if pygame.sprite.collide_mask(self, hero):
            coins_sprites.remove(self)
            all_sprites.remove(self)
            kolvo_coins += 1


class Plus_HP(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((100, 100))
        self.rect = pygame.Rect(4, 400, 100, 100)

    def update(self):
        self.image.fill((249, 215, 28))
        font = pygame.font.Font('interface/fonts/static/Unbounded-Bold.ttf', 36)
        text = font.render('+', True,
                           'black')
        self.image.blit(text, (40, 20))


def load_coins():
    global kolvo_coins
    con = sqlite3.connect(r"./config/data_base.db3")
    cur = con.cursor()
    kolvo_coins = cur.execute('SELECT number_of_points FROM Player_records').fetchone()[0]
    cur.close()


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.coin_flag = True
        self.image = pygame.Surface((100, 100))
        self.rect = pygame.Rect(4, 200, 100, 100)
        # pygame.draw.rect(self.image, (255, 255, 255), self.rect, 100, 2)

    def update(self):
        f1 = pygame.font.Font('interface/fonts/static/Unbounded-Black.ttf', 16)
        f2 = pygame.font.Font('interface/fonts/static/Unbounded-Bold.ttf', 36)
        self.image.fill((0, 0, 0))
        text1 = f1.render(f'MOHET:', True,
                          'red')
        text2 = f2.render(str(kolvo_coins), True,
                          'red')
        self.image.blit(text1, (1, 1))
        self.image.blit(text2, (40, 40))


# Кастомизированный курсор


class Cursor(pygame.sprite.Sprite):
    if mode == 'normal':
        image = load_image("cursor.png")
    else:
        image = load_image("cursor_pixel.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()

    def update(self, position=None):
        if mode == 'normal':
            image = load_image("cursor.png")
        else:
            image = load_image("cursor_pixel.png")

        self.image = image

        if position is not None:
            self.rect.topleft = position


# ?
class EasterCar(pygame.sprite.Sprite):
    image = load_image(os.path.join('easter', "easter_car.png"))

    def __init__(self, position, *group):
        super().__init__(*group)
        self.image = EasterCar.image
        self.U = randint(6, 10)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        xu = 0
        if self.rect.x < 101:
            xu = 2
        elif self.rect.x > WIDTH - self.image.get_width() - 101:
            xu = -2
        self.rect = self.rect.move(xu, self.U)


def get_key(value):
    global custom_keys
    for key, name in keys.items():
        if name == value:
            return key


# Сердце игры - обработка событий


def main():
    global DOWN, UP, LEFT, RIGHT, hp, custom_keys, kolvo_coins
    hp = 3
    hero.restart_hero()
    pygame.mouse.set_visible(False)
    died_sound.stop()
    pygame.mixer.music.play(-1)
    load_coins()
    for asd in range(0, 99, 33):
        HitPoints((15 + asd, 330), all_sprites, hp_sprites)
    Plus_HP(all_sprites)
    running = True
    DOWN, UP, LEFT, RIGHT = False, False, False, False
    for _ in range(3):
        random_appearence(cars_sprites)

    # Ну а теперь обработка событий - на что нажал пользователь, куда и т.д.
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == get_key(custom_keys[0]):
                    UP = True
                if event.key == get_key(custom_keys[2]):
                    LEFT = True
                if event.key == get_key(custom_keys[1]):
                    DOWN = True
                if event.key == get_key(custom_keys[3]):
                    RIGHT = True
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYUP:
                if event.key == get_key(custom_keys[0]):
                    UP = False
                if event.key == get_key(custom_keys[2]):
                    LEFT = False
                if event.key == get_key(custom_keys[1]):
                    DOWN = False
                if event.key == get_key(custom_keys[3]):
                    RIGHT = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                xcross.update(True)
                if cursor.rect.topleft[0] in range(4, 104) and cursor.rect.topleft[1] in range(400, 500):
                    if kolvo_coins >= 10:
                        kolvo_coins -= 10
                        hp += 1
                        HitPoints((hp_sprites.sprites()[-1].rect.topleft[0] + 53, 330), all_sprites, hp_sprites)
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
        for car in cars_sprites:
            if car.rect.y >= HEIGHT:
                cars_sprites.remove(car)
                all_sprites.remove(car)
                random_appearence(cars_sprites)
                if randint(1, 5) == 1:
                    random_appearence(cars_sprites, True)
        update_background()
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    terminate()


if __name__ == '__main__':
    # Создаем нужные группы спрайтов
    all_sprites = pygame.sprite.Group()
    cars_sprites = pygame.sprite.Group()
    easter_sprite = pygame.sprite.Group()
    coins_sprites = pygame.sprite.Group()
    hp_sprites = pygame.sprite.Group()
    # ?
    easter_flag = True
    # Объявляем нужные переменные и создаем все нужные спрайты
    DOWN, UP, LEFT, RIGHT = False, False, False, False
    clock = pygame.time.Clock()
    scoreboard = Scoreboard(all_sprites)
    hero = Hero(all_sprites)
    game_over_flag = False
    cursor = Cursor(all_sprites)
    xcross = Xcross(all_sprites)
    main_menu()
