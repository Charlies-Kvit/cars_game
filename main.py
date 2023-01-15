import pygame
import os
import sys

pygame.init()
pygame.display.set_caption('')
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)


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


def terminate():
    pygame.quit()
    sys.exit()


class Road(pygame.sprite.Sprite):
    image = load_image('road.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Road.image
        self.rect = self.image.get_rect()


class Hero(pygame.sprite.Sprite):
    image = load_image('hero_car.png')

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.U = 1
        self.rect.x = WIDTH / 2 - 15
        self.rect.y = HEIGHT / 4 * 3 - 15

    def update(self):
        global UP, DOWN, RIGHT, LEFT
        for car in cars_sprites:
            if pygame.sprite.collide_mask(self, car):
                print('Game over')
                terminate()
            if UP:
                self.rect = self.rect.move(0, -self.U)
            if DOWN:
                self.rect = self.rect.move(0, self.U)
            if LEFT:
                self.rect = self.rect.move(-self.U, 0)
            if RIGHT:
                self.rect = self.rect.move(self.U, 0)


class Car(pygame.sprite.Sprite):
    image = load_image(os.path.join('cars', 'tow_truck1.png'))

    def __init__(self, position, *group):
        super().__init__(*group)
        self.image = Car.image
        self.U = 1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        self.rect = self.rect.move(0, self.U)


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    road_sprite = pygame.sprite.Group()
    cars_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    Road(all_sprites, road_sprite)
    Hero(all_sprites, hero_sprite)
    Car((10, 10), all_sprites, cars_sprites)
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    UP = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    LEFT = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    DOWN = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    RIGHT = False
        all_sprites.update()
        screen.fill('black')
        all_sprites.draw(screen)
        clock.tick(120)
        pygame.display.flip()
    pygame.quit()
