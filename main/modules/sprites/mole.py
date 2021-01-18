
import pygame


class Mole(pygame.sprite.Sprite):
    def __init__(self, image_paths, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(image_paths[0]), (101, 103)), 
                       pygame.transform.scale(pygame.image.load(image_paths[-1]), (101, 103))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.setPosition(position)
        self.is_hammer = False

    def setPosition(self, pos):
        self.rect.left, self.rect.top = pos

    def setBeHammered(self):
        self.is_hammer = True

    def draw(self, screen):
        if self.is_hammer: self.image = self.images[1]
        screen.blit(self.image, self.rect)

    def reset(self):
        self.image = self.images[0]
        self.is_hammer = False