from random import randint, choice
import pygame
import os
import sys

road = pygame.image.load('interface/road.png')
pygame.init()
pygame.display.set_caption('')
size = WIDTH, HEIGHT = road.get_size()
screen = pygame.display.set_mode(size)
cars_images = os.listdir('interface/cars')
y1 = 0
y2 = -HEIGHT


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
  
  
def random_appearence(over_cars, ccc=False):
    global easter_flag
    over_cars_cords = []
    for i in over_cars:
        if i.rect.topleft[1] <= 520:
            over_cars_cords.append((i.rect.topleft[0], i.rect.topright[0]))
    print(over_cars_cords)
    # thirst, second, third = range(0, 233), range(234, 466), range(467, 700)
    asd = 0
    flag = True
    while flag:
        x = randint(100, WIDTH - 229)
        asd += 1
        with open('logs/logs.txt', 'a') as w:
            w.write(str(x) + ' ' + str(asd) + '\n')
        kol_vo_sovp = 0
        for i in over_cars_cords:
            if x not in range(i[0], i[1] + 1) and x + 120 not in range(i[0], i[1] + 1):
                kol_vo_sovp += 1
        if kol_vo_sovp == len(over_cars_cords):
            print(x, x + 119)
            if randint(1, 100) != 0 and easter_flag:
                EasterCar((x, -300), all_sprites, cars_sprites, easter_sprite)
                easter_flag, flag = False, False
                continue
            if ccc:
                Coin((x, -300), all_sprites, coins_sprites)
            else:
                if randint(1, 4) == 4:
                    print('УРА ГРУЗОВИК!')
                    Gruzovik((x, -500), all_sprites, cars_sprites)
                else:
                    Car((x, -300), all_sprites, cars_sprites)
            flag = False
            break
        else:
            kol_vo_sovp = 0


def terminate():
    pygame.quit()
    sys.exit()


class Xcross(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.Surface((2 * 10, 2 * 10),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (10, 10), 10)
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.centerx = WIDTH - 15
        self.rect.centery = 55

    def update(self, pos=None):
        if pos is None:
            return


class Hero(pygame.sprite.Sprite):
    image = load_image('hero_car.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.U = 6
        self.rect.centerx = WIDTH / 2 - 15
        self.rect.centery = HEIGHT / 4 * 3 - 15

    def update(self):
        global UP, DOWN, RIGHT, LEFT
        for auto_car in cars_sprites.sprites():
            if pygame.sprite.collide_mask(self, auto_car):
                if auto_car in easter_sprite:
                    from easter_game import start_easter_egg
                    pygame.quit()
                    pygame.init()
                    start_easter_egg()
                    sys.exit()
                print('Game over')
                terminate()
        if UP and self.rect.y > 0:
            self.rect = self.rect.move(0, -self.U)
        if DOWN and self.rect.y < HEIGHT - self.image.get_height():
            self.rect = self.rect.move(0, self.U)
        if LEFT and self.rect.x > 101:
            self.rect = self.rect.move(-self.U, 0)
        if RIGHT and self.rect.x < WIDTH - self.image.get_width() - 101:
            self.rect = self.rect.move(self.U, 0)


class Car(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        self.image = load_image(os.path.join('cars', choice(cars_images)))
        self.U = randint(5, 10)
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


class Gruzovik(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        self.coin_flag = True
        self.image = load_image(os.path.join('cars', 'gruz.png'))
        self.U = randint(10, 15)
        sound1 = pygame.mixer.Sound('interface/gudok.ogg')
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


class Coin(pygame.sprite.Sprite):
    def __init__(self, position, *group):
        super().__init__(*group)
        self.coin_flag = True
        self.image = load_image('coin.png')
        self.U = 5
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        global kolvo_coins
        xu = 0
        if self.rect.x < 101:
            xu = 2
        elif self.rect.x > WIDTH - self.image.get_width() - 101:
            xu = -2
        self.rect = self.rect.move(xu, self.U)

        for auto_car in hero_sprite.sprites():
            if pygame.sprite.collide_mask(self, auto_car):
                coins_sprites.remove(self)
                all_sprites.remove(self)
                kolvo_coins += 1
                print(kolvo_coins)
        

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


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    road_sprite = pygame.sprite.Group()
    cars_sprites = pygame.sprite.Group()
    xcross_sprite = pygame.sprite.Group()
    easter_sprite = pygame.sprite.Group()
    coins_sprites = pygame.sprite.Group()
    easter_flag = True
    kolvo_coins = 0
    clock = pygame.time.Clock()
    running = True
    Hero(all_sprites, hero_sprite), Xcross(all_sprites)
    for i in range(3):
        random_appearence(cars_sprites)
    DOWN, UP, LEFT, RIGHT = False, False, False, False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    UP = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    LEFT = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    DOWN = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    RIGHT = True
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    UP = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    LEFT = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    DOWN = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    RIGHT = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                xcross_sprite.update(event.pos)
        for car in cars_sprites:
            if car.rect.y >= HEIGHT:
                cars_sprites.remove(car)
                all_sprites.remove(car)
                random_appearence(cars_sprites)
                if randint(1, 5) < 10:
                    print("MONEY!!!")
                    random_appearence(cars_sprites, True)
        all_sprites.update()
        update_background()
        all_sprites.draw(screen)
        clock.tick(120)
        pygame.display.flip()
    pygame.quit()
