import pygame
from button import Button
from image import Image, BodyPart
from drawing_board import DrawingBoard

pygame.init()

(width, height) = (400, 600)
screen = pygame.display.set_mode((width, height))
game_font = pygame.font.SysFont('Comic Sands MS', 30)
clock = pygame.time.Clock()
running = True

head = BodyPart(surface = screen)
head.pixels = [
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()],
                    [None, None, None, None, None, (), (), (), (), (), (), None, None, None, None, None],
                    [None, None, None, None, None, (), (), (), (), (), (), None, None, None, None, None],
                    [None, None, None, None, None, (), (), (), (), (), (), None, None, None, None, None],
                    [None, None, None, None, None, (), (), (), (), (), (), None, None, None, None, None]                    
            ]
            
head.scale(10)
head.scale_factor = 2

game_objects = {
    'plain_body': Image(screen, 'plain_body.png'),
    'back_button': Button(screen, 10, 550, 100, 40, 'back', False),
    'head_button': Button(screen, 150, 420, 100, 40, 'head'), 
    'torso_button': Button(screen, 150, 480, 100, 40, 'torso'),
    'larm_button': Button(screen, 10, 480, 100, 40, 'left arm'),
    'rarm_button': Button(screen, 290, 480, 100, 40, 'right arm'),
    'lower_button': Button(screen, 150, 540, 100, 40, 'lower'),
    'head_drawing_board': DrawingBoard(screen, 20, 20, 360, 360, 'draw here', False, 20, head),
}

def display_mouse_pos():
    x, y = pygame.mouse.get_pos()
    txt_mouse_pos = game_font.render('{}, {}'.format(x, y), True, (255, 255, 255))
    screen.blit(txt_mouse_pos, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                 
        
        if event.type == pygame.KEYDOWN:
            if game_objects['head_drawing_board'].visible: game_objects['head_drawing_board'].handle_all_events(key = event.key, unicode = event.unicode)
                
            mouse_pos = pygame.mouse.get_pos()
            length = 0
            prev_not_black = False
            if event.key == pygame.K_UP:
                for x in range(mouse_pos[0], width):
                    pixel_color = screen.get_at((x, mouse_pos[1]))
                    if pixel_color != (0, 0, 0):
                        prev_not_black = True
                        length += 1  
                    if pixel_color == (0, 0, 0) and prev_not_black:
                        break;
            if event.key == pygame.K_DOWN:
                for y in range(mouse_pos[1], height):
                    pixel_color = screen.get_at((mouse_pos[0], y))
                    if pixel_color != (0, 0, 0):
                        prev_not_black = True
                        length += 1  
                    if pixel_color == (0, 0, 0) and prev_not_black:
                        break;                            
            print(length)
                        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_objects['head_button'].collide(event.pos):
                for name, obj in game_objects.items(): obj.visible = False
                game_objects['back_button'].visible = True
                game_objects['head_drawing_board'].visible = True
        
            if game_objects['back_button'].collide(event.pos):
                for name, obj in game_objects.items(): obj.visible = True
                game_objects['back_button'].visible = False
                game_objects['head_drawing_board'].visible = False
                
            if game_objects['head_drawing_board'].visible: game_objects['head_drawing_board'].handle_all_events(event.pos, "msb_down")
                
        if event.type == pygame.MOUSEBUTTONUP:
            if game_objects['head_drawing_board'].visible: game_objects['head_drawing_board'].handle_all_events(event.pos, "msb_up")
        
        
    screen.fill((0, 0, 0))    
    display_mouse_pos()
    for name, obj in game_objects.items(): 
        if obj.visible: obj.draw()
        #if game_objects['head_drawing_board'].visible == False: game_objects['head_drawing_board'].draw_compressed_image(160, 40)
        
    pygame.display.update()
    clock.tick(60)  