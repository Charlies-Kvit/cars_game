import pygame
import os
import sys

if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    road_sprite = pygame.sprite.Group()
    cars_sprites = pygame.sprite.Group()
    pygame.display.set_caption('')
    size = WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

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
            self.rect.x = WIDTH / 2 - 15
            self.rect.y = HEIGHT / 4 * 3 - 15

        def update(self, cords=None):
            if cords is not None:
                self.rect = self.rect.move(cords[0], cords[1])

    running = True
    Road(all_sprites, road_sprite)
    Hero(all_sprites, hero_sprite)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    hero_sprite.update((0, -10))
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    hero_sprite.update((-10, 0))
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    hero_sprite.update((0, 10))
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    hero_sprite.update((10, 0))
        all_sprites.update()
        screen.fill('white')
        all_sprites.draw(screen)
        clock.tick(120)
        pygame.display.flip()
    pygame.quit()
