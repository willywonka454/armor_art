import pygame

class Image:
    def __init__(self, surface = None, addr = 'default_img.png', x = 0, y = 0, visible = True):
        self.surface = surface; self.addr = addr; self.x = x; self.y = y; self.visible = visible
        self.internal_image = pygame.image.load(self.addr)
        
    def draw(self, surface = None, x = None, y = None):        
        if x == None: x = self.x 
        if y == None: y = self.y
        if surface == None: surface = self.surface
        self.surface.blit(self.internal_image, (x, y))
        
class BodyPart:
    def __init__(self, surface = None, x = 0, y = 0, visible = True, color = (236, 188, 180)):
        self.surface = surface; self.x = x; self.y = y 
        self.visible = visible; self.color = color
        self.pixels = [[self.color]]
        self.max_w = 0
        self.max_h = 0
        self.scale_factor = 0
    
    def deep_copy(self):
        new_bp = BodyPart(self.surface, self.x, self.y, self.visible, self.color)
        
    
    def update_max_width(self):
        for row in range(len(self.pixels)):
            if len(self.pixels[row]) > self.max_w: self.max_w = len(self.pixels[row])                
        
    def update_max_height(self):
        self.max_h = len(self.pixels)
        
    def scale(self, scale_factor):
        new_pixels = self.scale_arr(self.pixels, scale_factor)
        for row in range(len(new_pixels)): new_pixels[row] = self.scale_arr(new_pixels[row], scale_factor)
        self.pixels = new_pixels
        self.update_max_width()
        self.update_max_height()
    
    def scale_arr(self, arr, scale_factor):
        new_arr = [None for cell in range( int(len(arr) * scale_factor) )]
        index_of_val_to_copy = 0
        index_of_new_val = 0
        while(index_of_val_to_copy < len(arr)):
            start_index = index_of_new_val
            while(index_of_new_val < start_index + scale_factor):
                new_arr[index_of_new_val] = arr[index_of_val_to_copy]
                index_of_new_val += 1
            index_of_val_to_copy += 1            
        return new_arr
        
    def draw(self):
        for row in range(len(self.pixels)):
            for col in range(len(self.pixels[row])):
                if self.pixels[row][col] != None: self.surface.set_at((self.x + col, self.y + row), self.color)                                   