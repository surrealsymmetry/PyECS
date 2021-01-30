import pygame
import rack
import ECS_Inspector as tools

pygame.init()
screen = pygame.display.set_mode((640, 480))
background = pygame.Surface(screen.get_size())
background.fill((115, 100, 128))
background = background.convert()
screen.blit(background, (0,0))
clock = pygame.time.Clock()

mainloop = True
e_timer = rack.e(rack.c("pygame_global_timer"))

def run():
    global mainloop
    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
        screen.blit(background, (0, 0))
        rack.update()
        text = ":FPS: {0:.2f} Playtime: {1:.2f}".format(clock.get_fps(), e_timer.components["pygame_global_timer"].total)
        pygame.display.set_caption(text)
        pygame.display.flip()