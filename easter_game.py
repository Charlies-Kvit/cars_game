import pygame
import pytmx
import sys
import os

pygame.init()
size = WIDTH, HEIGHT = 800, 800
DOWN, UP, LEFT, RIGHT = False, False, False, False
pygame.mixer.music.load(os.path.join("interface", "easter", "sounds", "scare_music.mp3"))
pygame.mixer.music.play()
children_laughter = pygame.mixer.Sound(os.path.join("interface/easter/sounds/laugh.mp3"))
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
crying_children = pygame.sprite.Group()


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


class CryingBaby(pygame.sprite.Sprite):
    image = load_image(os.path.join("easter", "easter_cry_child.png"))

    def __init__(self, cords, *group):
        super().__init__(*group)
        self.image = CryingBaby.image
        self.rect = self.image.get_rect()
        self.rect.x = cords[0]
        self.rect.y = cords[1]


class Hero(pygame.sprite.Sprite):
    image = load_image(os.path.join('easter', "easter_hero.png"))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 49
        self.rect.y = 49
        self.U = 1

    def update(self, level=None):
        global UP, DOWN, RIGHT, LEFT, children_laughter
        for baby in crying_children.sprites():
            if pygame.sprite.collide_mask(self, baby):
                children_laughter.play()
                crying_children.remove(baby)
                all_sprites.remove(baby)
        if level is not None:
            ux, uy = 0, 0
            x, y = self.rect.x, self.rect.y
            if UP and self.rect.y > 0:
                uy -= self.U
            if DOWN and self.rect.y < HEIGHT - self.image.get_height():
                uy += self.U
            if LEFT and self.rect.x > 0:
                ux -= self.U
            if RIGHT and self.rect.x < WIDTH - self.image.get_width():
                ux += self.U
            if level.is_free((x + ux, y + uy)):
                self.rect = self.rect.move(ux, uy)
        if 385 <= self.rect.x <= 400 and 680 <= self.rect.y <= 695:
            pygame.mixer.music.stop()
            if crying_children.sprites():
                flag = False
            else:
                flag = True
            pygame.quit()
            scary_function(flag)
            sys.exit()


class Map:
    def __init__(self):
        self.map = pytmx.load_pygame(os.path.join("maps", "easter_map.tmx"))
        self.map_matrix = [[0] * HEIGHT for _ in range(WIDTH)]
        print(len(self.map_matrix), len(self.map_matrix[0]))
        self.flag = True
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth

    def render(self, screen):
        for i in range(4):
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image is not None:
                        if 1 <= i <= 2 and self.flag:
                            self.map_matrix[x][y] = 1
                        screen.blit(image, (x * self.tile_size, y * self.tile_size))
        self.flag = False

    def is_free(self, position):
        flag = True
        x, y = int((position[0] / 16)), int((position[1] / 16)) + 1
        if self.map_matrix[x][y] != 0:
            flag = False
        return flag


class Video(object):
    def __init__(self, path):
        self.path = path

    def play(self):
        os.startfile(self.path)


class Movie_MP4(Video):
    type = "MP4"


def start_easter_egg():
    global DOWN, UP, RIGHT, LEFT
    clock = pygame.time.Clock()
    cords = [(607, 15), (774, 127), (369, 707), (16, 369), (753, 752)]
    for position in cords:
        CryingBaby(position, all_sprites, crying_children)
    Hero(all_sprites)
    maper = Map()
    running = True
    while running:
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    UP = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    LEFT = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    DOWN = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    RIGHT = True
                """if event.key == pygame.K_ESCAPE:
                    running = False"""
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    UP = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    LEFT = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    DOWN = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    RIGHT = False
        screen.fill((0, 0, 0))
        maper.render(screen)
        all_sprites.update(maper)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()


def scary_function(flag):
    if flag:
        path = os.path.join("interface", "easter", "MICHAEL.mp4")
    else:
        path = os.path.join("interface", "easter", "Are_you_sure_it's_not_your_fault.mp4")
    movie = Movie_MP4(path)
    movie.play()


start_easter_egg()
# scary_function()
