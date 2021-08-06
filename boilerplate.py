import pygame

(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                              
    
    screen.fill((0, 0, 0))
    
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
quit()    