import pygame
import settings

class Utility:
    def measure_distance(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2        
        x_dist = abs(x1 - x2)
        y_dist = abs(y1 - y2)
        return x_dist, y_dist
        
    def find_left_corner(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        left_most_x = x1 if x1 < x2 else x2
        top_most_y = y1 if y1 < y2 else y2
        return (left_most_x, top_most_y)
    
    def return_rect_dimensions(pos1, pos2):
        w, h = Utility.measure_distance(pos1, pos2)
        x, y = Utility.find_left_corner(pos1, pos2)
        return (x, y, w, h)

class GameObject:
    def __init__(self, surface, x, y, w, h, color, visible):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.surface, self.color, self.visible = surface, color, visible
    
    def change_vis(self, new_vis):
        self.visible = new_vis
    
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

    def create_copy(self):
        pass

class MyImage(GameObject):
    def __init__(self, surface, addr, x, y, visible):
        self.addr = addr
        self.internal_image = pygame.image.load(self.addr)
        GameObject.__init__(self, surface, x, y, self.internal_image.get_width(), self.internal_image.get_height(), None, visible)
        
    def draw(self):        
        self.surface.blit(self.internal_image, (self.x, self.y))  

class MySurface(GameObject):
    def __init__(self, surface, x, y, w, h, color, visible, transparent = False):
        GameObject.__init__(self, surface, x, y, w, h, color, visible)
        self.transparent = transparent
        if self.transparent == False: self.internal_surface = pygame.Surface((self.w, self.h))
        else: self.internal_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.my_perm_objects = []
        self.my_temp_objects = []
    
    def pop_temp_object(self):
        if len(self.my_temp_objects) > 0: self.my_temp_objects.pop()
        else: return None
    
    def change_size(self, new_w, new_h):
        GameObject.change_size(self, new_w, new_h)
        del self.internal_surface
        self.internal_surface = pygame.Surface((new_w, new_h))  
    
    def scale(self, scale_factor):
        new_w, new_h = int(self.w * scale_factor), int(self.h * scale_factor)
        self.change_size(new_w, new_h)        
        for obj in self.my_perm_objects: 
            obj.scale(scale_factor);
            new_x, new_y = int(obj.x * scale_factor), int(obj.y * scale_factor)
            obj.change_pos(new_x, new_y)
        for obj in self.my_temp_objects: 
            obj.scale(scale_factor);
            new_x, new_y = int(obj.x * scale_factor), int(obj.y * scale_factor)
            obj.change_pos(new_x, new_y)
    
    def draw(self):
        self.surface.blit(self.internal_surface, (self.x, self.y))
        if self.color: self.internal_surface.fill(self.color)
        else: self.internal_surface.fill((0, 0, 0, 0))
        for obj in self.my_perm_objects: 
            if obj.visible: obj.draw()
        for obj in self.my_temp_objects:
            if obj.visible: obj.draw()

    def blit(self, obj, pos):
        self.internal_surface.blit(obj, (pos)) 

    def create_copy(self):
        new_surface = MySurface(self.surface, self.x, self.y, self.w, self.h, self.color, self.visible, self.transparent)
        for obj in self.my_perm_objects: new_surface.my_perm_objects.append(obj.create_copy())
        for obj in self.my_temp_objects: new_surface.my_temp_objects.append(obj.create_copy())
        return new_surface
        
class DrawingArea(GameObject):
    def __init__(self, surface, x, y, w, h, color, visible, save_area = None):
        GameObject.__init__(self, surface, x, y, w, h, color, visible)
        self.canvas = MySurface(surface, x, y, w, h, color, True)
        self.gui = self.set_up_gui()   
        self.pen = {'color': (255, 0, 0), 'last_msb_down': None, 'last_msb_up': None}
        self.save_area = save_area

    def draw(self):
        self.canvas.draw()
        for name, obj in self.gui.items(): obj.draw()     
    
    def import_canvas(self, new_canvas):
        scale_factor = self.w / new_canvas.w
        buffer = new_canvas.create_copy()
        buffer.scale(scale_factor)
        for obj in buffer.my_perm_objects:
            obj.surface = self.canvas.internal_surface
            self.canvas.my_perm_objects.append(obj.create_copy())
            
    def save(self):
        scale_factor = self.save_area.w / self.w
        buffer = self.canvas.create_copy()
        buffer.scale(scale_factor)
        self.save_area.my_temp_objects.clear()
        for obj in buffer.my_temp_objects: 
            obj.surface = self.save_area.internal_surface
            self.save_area.my_temp_objects.append(obj.create_copy())
    
    def event_handler(self, pygame_event):
        self.handle_paint_event(pygame_event)
        self.handle_gui_event(pygame_event)   
    
    def handle_paint_event(self, pygame_event):
        if (pygame_event.type != pygame.MOUSEBUTTONDOWN and pygame_event.type != pygame.MOUSEBUTTONUP): return
        if self.canvas.collide(pygame_event.pos) == False: return
        if settings.waiting_for_color or settings.waiting_for_sample: return
        mouse_x, mouse_y = pygame_event.pos[0] - self.canvas.x, pygame_event.pos[1] - self.canvas.y
        the_grid = [
            (0, 19), (20, 39), (40, 59), (60, 79), (80, 99), (100, 119), (120, 139), (140, 159), (160, 179),
            (180, 199), (200, 219), (220, 239), (240, 259), (260, 279), (280, 299), (300, 319), (320, 339), (340, 359)
        ]
        for square in the_grid:
            lower_bound, upper_bound = (0, 1)
            if mouse_x >= square[lower_bound] and mouse_x <= square[upper_bound]: mouse_x = square[lower_bound]
            if mouse_y >= square[lower_bound] and mouse_y <= square[upper_bound]: mouse_y = square[lower_bound]
        if pygame_event.type == pygame.MOUSEBUTTONDOWN: self.pen['last_msb_down'] = (mouse_x, mouse_y)              
        else:
            if self.pen['last_msb_down'] == None: return
            self.pen['last_msb_up'] = (mouse_x, mouse_y)
            x, y, w, h = Utility.return_rect_dimensions(self.pen['last_msb_down'], self.pen['last_msb_up'])            
            self.canvas.my_temp_objects.append(MyRectangle(self.canvas.internal_surface, x, y, w + 20, h + 20, self.pen['color'], True)) 
            
    def handle_gui_event(self, pygame_event):
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
            if settings.waiting_for_sample:
                self.pen['color'] = self.surface.get_at(pygame_event.pos)
                settings.waiting_for_sample = False
            elif settings.waiting_for_color:
                for name, obj in self.gui.items():
                    if isinstance(obj, ColorButton): obj.active = False
                self.gui['r'].collide(pygame_event.pos), self.gui['g'].collide(pygame_event.pos), self.gui['b'].collide(pygame_event.pos)
            else:
                if self.gui['undo_button'].collide(pygame_event.pos): self.canvas.pop_temp_object()
                if self.gui['clear_button'].collide(pygame_event.pos): self.canvas.my_temp_objects.clear()
                if self.gui['save_button'].collide(pygame_event.pos): self.save()
                if self.gui['sample_button'].collide(pygame_event.pos): 
                    settings.waiting_for_sample = True; 
                    self.pen['last_msb_down'] = None
                for name, obj in self.gui.items():
                    if isinstance(obj, ColorButton): obj.active = False
                r, g, b = self.gui['r'].collide(pygame_event.pos), self.gui['g'].collide(pygame_event.pos), self.gui['b'].collide(pygame_event.pos)            
                if r or g or b: settings.waiting_for_color = True
        if pygame_event.type == pygame.KEYDOWN:
            for name, obj in self.gui.items():
                if obj.active and isinstance(obj, ColorButton):
                    finished_changing_color = obj.key_down(pygame_event)
                    if finished_changing_color:
                        new_color = self.gui['r'].return_int(), self.gui['g'].return_int(), self.gui['b'].return_int()
                        self.pen['color'] = new_color
                        settings.waiting_for_color = False
                        
    
    def set_up_gui(self):
        button_color = (128, 128, 128)
        new_gui = {
            'undo_button': MyButton(self.surface, self.x + 120, self.y + self.h + 60, 100, 40, "undo", button_color, True),
            'clear_button': MyButton(self.surface, self.x + 240, self.y + self.h + 60, 100, 40, "clear", button_color, True),
            'save_button': MyButton(self.surface, self.x, self.y + self.h + 110, 100, 40, "save", button_color, True),
            'sample_button': MyButton(self.surface, self.x, self.y + self.h + 60, 100, 40, "sample", button_color, True),            
            'r': ColorButton(self.surface, self.x, self.y + self.h + 10, 100, 40, 'r', 'red', True),
            'g': ColorButton(self.surface, self.x + 120, self.y + self.h + 10, 100, 40, 'g', 'green', True),
            'b': ColorButton(self.surface, self.x + 240, self.y + self.h + 10, 100, 40, 'b', 'blue', True)
        }
        return new_gui
        
class MyRectangle(GameObject):
    def __init__(self, surface, x, y, w, h, color, visible):
        GameObject.__init__(self, surface, x, y, w, h, color, visible)
        self.internal_rect = pygame.Rect(x, y, w, h)
    
    def change_pos(self, new_x, new_y):
        GameObject.change_pos(self, new_x, new_y)
        self.internal_rect.x = new_x; self.internal_rect.y = new_y
    
    def change_size(self, new_w, new_h):
        GameObject.change_size(self, new_w, new_h)
        self.internal_rect.w, self.internal_rect.h = new_w, new_h
    
    def scale(self, scale_factor):
        new_w, new_h = int(self.w * scale_factor), int(self.h * scale_factor)
        self.change_size(new_w, new_h)
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.internal_rect)

    def create_copy(self):
        return MyRectangle(self.surface, self.x, self.y, self.w, self.h, self.color, self.visible)
        
class MyButton(MyRectangle):
    def __init__(self, surface, x, y, w, h, text, color, visible, active = False):
        MyRectangle.__init__(self, surface, x, y, w, h, color, visible)
        self.text = text
        self.active = active
    
    def collide(self, event_pos):
        collision_occured = GameObject.collide(self, event_pos)
        if collision_occured: self.active = True
        return collision_occured
    
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

class ColorButton(MyButton):
    def __init__(self, surface, x, y, w, h, text, color, visible, active = False):
        MyButton.__init__(self, surface, x, y, w, h, text, color, visible)
        self.first_keydown = False
    
    def collide(self, event_pos):
        collision_occured = MyButton.collide(self, event_pos)
        if collision_occured: self.first_keydown = True
        return collision_occured
        
    def key_down(self, pygame_event):
        finished_changing_color = False        
        if self.active:
            if self.first_keydown and pygame_event.key != pygame.K_RETURN: self.text = ''
            if pygame_event.key == pygame.K_DELETE: self.text = ''
            elif pygame_event.key == pygame.K_RETURN: 
                self.active = False
                finished_changing_color = True
            elif pygame_event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            else: self.text += pygame_event.unicode;
        self.first_keydown = False
        return finished_changing_color
        
    def return_int(self):
        color_val = 0
        try: color_val = int(self.text)
        except: pass
        if color_val < 0: color_val = 0
        if color_val > 255: color_val = 255
        self.text = str(color_val)
        return color_val