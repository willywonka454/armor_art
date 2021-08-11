import pygame

class Image:
    def __init__(self, surface = None, addr = 'default_img.png', x = 0, y = 0, visible = True):
        self.surface = surface; self.addr = addr; self.x = x; self.y = y; self.visible = visible
        self.internal_image = pygame.image.load(self.addr)
        
    def draw(self):        
        self.surface.blit(self.internal_image, (self.x, self.y))      