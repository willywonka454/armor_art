import pygame

class Button:
    def __init__(self, surface = None, x = 0, y = 0, width = 100, height = 40, text = None, visible = True, color = (128, 128, 128), active = False):
        self.surface = surface; self.x = x; self.y = y
        self.width = width; self.height = height; 
        self.text = text; self.visible = visible; self.color = color
        self.active = active
        self.internal_rect = pygame.Rect(x, y, self.width, self.height)
    
    def draw(self, surface = None, x = None, y = None, text = None):
        if surface == None: surface = self.surface
        if x == None: x = self.x 
        if y == None: y = self.y 
        if text == None: text = self.text
        pygame.draw.rect(self.surface, self.color, self.internal_rect)
        if text != None:
            font = pygame.font.SysFont('Comic Sands MS', 30)
            button_text = font.render(text, True, (255, 255, 255))
            coords = self.center_text(button_text)
            self.surface.blit(button_text, coords)        
    
    def modify_pos(self, x, y):
        self.x = x; self.y
        self.internal_rect.x = x; self.internal_rect.y = y
    
    def collide(self, event_pos):
        if self.internal_rect.collidepoint(event_pos) and self.visible: self.active = True; return True
        return False
        
    def center_text(self, button_text): 
        center_x = self.x + (self.width - button_text.get_rect().width) / 2
        center_y = self.y + (self.height - button_text.get_rect().height) / 2
        return (center_x, center_y)
        
    def __repr__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.width)