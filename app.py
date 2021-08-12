import pygame
from useful_objects import*

pygame.init()

(width, height) = (400, 600)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
game_font = pygame.font.SysFont('Comic Sands MS', 30)
button_color = (128, 128, 128)

game_objects = {
    'head_save_area': MySurface(screen, 110, -10, 180, 180, (255, 0, 0), True),
    'torso_save_area': MySurface(screen, 110, 110, 180, 180, (0, 255, 0), True),
    'larm_save_area': MySurface(screen, 20, 60, 180, 180, (255, 0, 255), True),
    'rarm_save_area': MySurface(screen, 200, 60, 180, 180, (0, 0, 255), True),
    'lower_save_area': MySurface(screen, 110, 230, 180, 180, (0, 255, 255), True),
    'pixel_man': MyImage(screen, 'pixel_man.png', 0, 0, True),
    'back_button': MyButton(screen, 10, 550, 100, 40, 'back', button_color, False),
    'head_button': MyButton(screen, 150, 420, 100, 40, 'head', button_color, True), 
    'torso_button': MyButton(screen, 150, 480, 100, 40, 'torso', button_color, True),
    'larm_button': MyButton(screen, 10, 480, 100, 40, 'left arm', button_color, True),
    'rarm_button': MyButton(screen, 290, 480, 100, 40, 'right arm', button_color, True),
    'lower_button': MyButton(screen, 150, 540, 100, 40, 'lower', button_color, True),
    'head_drawing_area': DrawingArea(screen, 20, 20, 360, 360, button_color, False),
    'torso_drawing_area': DrawingArea(screen, 20, 20, 360, 360, button_color, False),
    'larm_drawing_area': DrawingArea(screen, 20, 20, 360, 360, button_color, False),
    'rarm_drawing_area': DrawingArea(screen, 20, 20, 360, 360, button_color, False),
    'lower_drawing_area': DrawingArea(screen, 20, 20, 360, 360, button_color, False)
}
                              
def display_mouse_pos():
    x, y = pygame.mouse.get_pos()
    txt_mouse_pos = game_font.render('{}, {}'.format(x, y), True, (255, 255, 255))
    screen.blit(txt_mouse_pos, (0, 0))

def go_to_drawing_area(button_clicked):
    area_selector = {
        'head_button': game_objects['head_drawing_area'],
        'torso_button': game_objects['torso_drawing_area'],
        'larm_button': game_objects['larm_drawing_area'],
        'rarm_button': game_objects['rarm_drawing_area'],
        'lower_button': game_objects['lower_drawing_area'],
    }
    for name, obj in game_objects.items():
        if obj.visible: obj.visible = False
    area_selector[button_clicked].visible = True
    game_objects['back_button'].visible = True

def go_to_main_menu():
    for name, obj in game_objects.items():
        if obj.visible: obj.visible = False
        elif isinstance(obj, MyButton) or isinstance(obj, MyImage) and name != "back_button": obj.visible = True
    
def draw_screen():
    screen.fill((0, 0, 0))
    for name, obj in game_objects.items(): 
        if obj.visible: obj.draw()
    display_mouse_pos()    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                 
        
        if event.type == pygame.KEYDOWN:       
            pass
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, obj in game_objects.items():
                if obj.collide(event.pos) and isinstance(obj, MyButton) and button_name != 'back_button': go_to_drawing_area(button_name)
                
            if game_objects['back_button'].collide(event.pos): go_to_main_menu()           
                
        if event.type == pygame.MOUSEBUTTONUP:
            pass
     
    draw_screen()
     
    pygame.display.update()
    clock.tick(60)  