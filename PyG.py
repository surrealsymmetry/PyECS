import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
background = pygame.Surface(screen.get_size())
background.fill((115, 100, 128))
background = background.convert()
screen.blit(background (0,0))

clock = pygame.time.Clock()

mainloop = True


while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    screen.blit(background, (0, 0))