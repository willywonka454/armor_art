import pygame

class GameObject:
    def __init__(self, surface, x, y, w, h, color, visible):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.surface, self.color, self.visible = surface, color, visible
    
    def change_pos(self, new_x, new_y):
        self.x, self.y = new_x, new_y
    
    def change_size(self, new_w, new_h):
        self.w, self.h = new_w, new_h
    
    def center_x(self, background_w):
        new_x = (background_w - self.w) / 2
        self.change_pos(new_x, self.y)
        
    def center_y(self, background_h):
        new_y = (background_h - self.h) / 2
        self.change_pos(self.x, new_y)
    
    def collide(self, event_pos):
        x, y = event_pos
        x_min, y_min = self.x, self.y 
        x_max, y_max = self.x + self.w, self.y + self.h
        if (x >= x_min and x <= x_max) and (y >= y_min and y <= y_max) and self.visible: return True
        else: return False
        
    def draw(self):
        pass

class MyImage(GameObject):
    def __init__(self, surface, addr, x, y, visible):
        self.addr = addr
        self.internal_image = pygame.image.load(self.addr)
        GameObject.__init__(self, surface, x, y, self.internal_image.get_width(), self.internal_image.get_height(), None, visible)
        
    def draw(self):        
        self.surface.blit(self.internal_image, (self.x, self.y))  

class MySurface(GameObject):
    def __init__(self, surface, x, y, w, h, color, visible):
        GameObject.__init__(self, surface, x, y, w, h, color, visible)        
        self.internal_surface = pygame.Surface((self.w, self.h))
        self.my_objects = {}
    
    def change_size(self, new_w, new_h):
        GameObject.change_size(self, new_w, new_h)
        del self.internal_surface
        self.internal_surface = pygame.Surface((new_w, new_h))

    def draw(self):
        self.surface.blit(self.internal_surface, (self.x, self.y))
        if self.color: self.internal_surface.fill(self.color)
        for key, obj in self.my_objects.items(): 
            if obj.visible: obj.draw()

    def blit(self, obj, pos):
        self.internal_surface.blit(obj, (pos)) 

class DrawingArea(GameObject):
    def __init__(self, surface, x, y, w, h, color, visible):
        GameObject.__init__(self, surface, x, y, w, h, color, visible)
        self.canvas = MySurface(surface, x, y, w, h, color, visible)
    
    def change_pos(self, new_x, new_y):
        GameObject.change_pos(self, new_x, new_y)
        self.canvas.change_pos(new_x, new_y)
        
    def draw(self):
        self.canvas.draw()
        
class MyRectangle(GameObject):
    def __init__(self, surface, x, y, w, h, color, visible):
        GameObject.__init__(self, surface, x, y, w, h, color, visible)
        self.internal_rect = pygame.Rect(x, y, w, h)
    
    def change_pos(self, new_x, new_y):
        GameObject.change_pos(self, new_x, new_y)
        self.internal_rect.x = new_x, self.internal_rect.y = new_y
    
    def change_size(self, new_w, new_h):
        GameObject.change_size(new_w, new_h)
        self.internal_rect.w, self.internal_rect.h = new_w, new_h
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.internal_rect)

class MyButton(MyRectangle):
    def __init__(self, surface, x, y, w, h, text, color, visible):
        MyRectangle.__init__(self, surface, x, y, w, h, color, visible)
        self.text = text
        
    def draw(self):
        MyRectangle.draw(self)
        if self.text != None:
            font = pygame.font.SysFont('Comic Sands MS', 30)
            button_text = font.render(self.text, True, (255, 255, 255))
            coords = self.center_text(button_text)
            self.surface.blit(button_text, coords)

    def center_text(self, button_text): 
        center_x = self.x + (self.w - button_text.get_rect().w) / 2
        center_y = self.y + (self.h - button_text.get_rect().h) / 2
        return (center_x, center_y)        