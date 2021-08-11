import pygame
from button import Button
from image import BodyPart

class DrawingBoard(Button):
    def __init__(self, surface = None, x = 0, y = 0, width = 100, height = 40, visible = True, pixel_width = 1):
        Button.__init__(self, surface, x, y, width, height, None, visible)
        self.pixel_width = pixel_width
        self.pixels = self.initialize_pixel_buttons()
        self.previous_colors = []
        self.gui = self.set_up_gui()
        self.pen_color = (255, 255, 255)
        self.msb_down = None; self.msb_up = None
        self.compressed_image = None
        
    def compress():
        pass
        
    def set_up_gui(self):
        gui_objects = {
            'undo_button': Button(self.surface, self.x + 120, self.y + self.height + 60, 100, 40, "undo", True),
            'clear_button': Button(self.surface, self.x + 240, self.y + self.height + 60, 100, 40, "clear", True),
            'save_button': Button(self.surface, self.x, self.y + self.height + 110, 100, 40, "save", True),
            'submit_color': Button(self.surface, self.x, self.y + self.height + 60, 100, 40, "submit", True),            
            'r': Button(self.surface, self.x, self.y + self.height + 10, 100, 40, "r", True),
            'g': Button(self.surface, self.x + 120, self.y + self.height + 10, 100, 40, "g", True),
            'b': Button(self.surface, self.x + 240, self.y + self.height + 10, 100, 40, "b", True)
        }
        return gui_objects
        
    def initialize_pixel_buttons(self):
        x_pixels = self.width // self.pixel_width
        y_pixels = self.height // self.pixel_width
        pixel_arr = [[Button(surface = self.surface, width = self.pixel_width, height = self.pixel_width) for columns in range(x_pixels)] for rows in range(y_pixels)]
        self.set_pixel_locations(pixel_arr)
        self.set_pixel_colors(pixel_arr)
        return pixel_arr
    
    def set_pixel_locations(self, pixel_arr):
        x_coord = self.x
        y_coord = self.y
        for i in range(len(pixel_arr)):
            for j in range(len(pixel_arr[i])):
                pixel_arr[i][j].modify_pos(x_coord, y_coord)
                x_coord += self.pixel_width
            y_coord += self.pixel_width
            x_coord = self.x
    
    def set_pixel_colors(self, pixel_arr):
        default_color = (128, 128, 128)
        alternate_color = (64, 64, 64)
        current_color = default_color
        prev_row_color = current_color
        for i in range(len(pixel_arr)):
            for j in range(len(pixel_arr[i])):
                if j == 0 and prev_row_color == default_color: 
                    current_color = alternate_color
                    prev_row_color = current_color
                elif j == 0 and prev_row_color == alternate_color:
                    current_color = default_color
                    prev_row_color = current_color
                elif current_color == default_color: current_color = alternate_color
                else: current_color = default_color
                pixel_arr[i][j].color = current_color
    
    def produce_path(self, origin, target):
        origin_loc = self.index_of_pixel_button(origin); origin_row = origin_loc['row']; origin_column = origin_loc['column']
        target_loc = self.index_of_pixel_button(target); target_row = target_loc['row']; target_column = target_loc['column']
        step = 1
        path = []
        if origin_row == target_row:
            if origin_column > target_column: step = -1
            for test_column in range(origin_column, target_column + step, step): path.append(self.pixels[origin_row][test_column])
        elif origin_column == target_column:
            if origin_row > target_row: step = -1
            for test_row in range(origin_row, target_row + step, step): path.append(self.pixels[test_row][origin_column])
        return path
    
    def index_of_pixel_button(self, pixel_button):
         for row in range(len(self.pixels)):
            for column in range(len(self.pixels[row])): 
                if self.pixels[row][column] == pixel_button: return {'row': row, 'column': column}
    
    def find_pixel_button_mathematically(self, x, y):
        pass
    
    def find_pixel_button_on_collision(self, event_pos):
        for row in range(len(self.pixels)):
            for column in range(len(self.pixels[row])): 
                if self.pixels[row][column].collide(event_pos): return self.pixels[row][column]
    
    def restore_previous_colors(self):
        if len(self.previous_colors) <= 0: return
        else:
            button_data = self.previous_colors.pop()
            for pixel_button in button_data: 
                pixel_button['button'].color = pixel_button['orig_color']
                pixel_button['button'].active = False
    
    def handle_all_events(self, event_pos = None, msb_click = None, key = None, unicode = None):
        if event_pos and self.collide(event_pos): self.handle_paint_event(event_pos, msb_click)
        else: self.handle_gui_event(event_pos, msb_click, key, unicode)
        
    def handle_gui_event(self, event_pos, msb_click = None, key = None, unicode = None):
        if msb_click == "msb_down":
            for name, obj in self.gui.items():
                if obj.collide(event_pos):
                    for other_names, other_obj in self.gui.items(): 
                        if (other_obj != obj) and other_obj.active: other_obj.active = False
            if self.gui['save_button'].collide(event_pos): self.compressed_image = self.compress();
            if self.gui['undo_button'].collide(event_pos): self.restore_previous_colors()
            if self.gui['r'].collide(event_pos): self.gui['r'].text = ""
            if self.gui['g'].collide(event_pos): self.gui['g'].text = ""
            if self.gui['b'].collide(event_pos): self.gui['b'].text = ""
            if self.gui['submit_color'].collide(event_pos): self.pen_color = (int(self.gui['r'].text), int(self.gui['g'].text), int(self.gui['b'].text))
        elif key != None:
            for name, obj in self.gui.items():
                if (name == 'r' or name == 'g' or name == 'b') and obj.active: self.handle_color_change_event(obj, key, unicode)            
        
    def handle_color_change_event(self, color_input_button, key, unicode):
        if key == pygame.K_DELETE: color_input_button.text = ""
        elif key == pygame.K_ESCAPE: color_input_button.active = False
        elif key == pygame.K_BACKSPACE: color_input_button.text = color_input_button.text[:-1]
        else: color_input_button.text += unicode
            
    def handle_paint_event(self, event_pos, msb_click):
        if msb_click == "msb_down":
            self.msb_down = self.find_pixel_button_on_collision(event_pos)
        else:
            self.msb_up = self.find_pixel_button_on_collision(event_pos)
            pixel_buttons_to_paint = self.produce_path(self.msb_down, self.msb_up)
            original_colors = []
            for pixel_button in pixel_buttons_to_paint:
                original_colors.append({'button': pixel_button, 'orig_color': pixel_button.color})
                pixel_button.color = self.pen_color
                pixel_button.active = True
            if len(original_colors) > 0: self.previous_colors.append(original_colors)
            
    def draw(self):
        active_pixel_buttons = []
        for i in range(len(self.pixels)):
            for j in range(len(self.pixels[i])): 
                if self.pixels[i][j].active: active_pixel_buttons.append(self.pixels[i][j])
                else: self.pixels[i][j].draw()
        for name, obj in self.gui.items(): obj.draw()
        if self.body_part: self.body_part.draw()
        for i in range(len(active_pixel_buttons)): active_pixel_buttons[i].draw()