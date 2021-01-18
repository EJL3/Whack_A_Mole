
import pygame


class Hammer(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(image_paths[0]), pygame.image.load(image_paths[1])]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.images[1])
        self.rect.left, self.rect.top = position

        self.hammer_count = 0
        self.hammer_last_time = 4
        self.is_hammering = False

    def setPosition(self, pos):
        self.rect.centerx, self.rect.centery = pos

    def setHammering(self):
        self.is_hammering = True

    def draw(self, screen):
        if self.is_hammering:
            self.image = self.images[1]
            self.hammer_count += 1
            if self.hammer_count > self.hammer_last_time:
                self.is_hammering = False
                self.hammer_count = 0
        else:
            self.image = self.images[0]
        screen.blit(self.image, self.rect)