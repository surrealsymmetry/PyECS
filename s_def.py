import rack
import PyG
import pygame
import ECS_Inspector as tools

def nudge_timer(e):
    c = e.components["timer"]
    c.delta = PyG.clock.tick(60)
    c.total += (c.delta / 1000)

def prep_sprites(e):
    color1 = (180, 255, 200)
    color2 = (255, 180, 200)
    lineweight = 3
    if 'sprite' not in e.components:
        sprite_surface = None
        if 'bounds' in e.components:
            #box entity
            width, height = e.components["bounds"].x, e.components["bounds"].y
            sprite_surface = pygame.Surface((width, height))
            pygame.draw.rect(sprite_surface, color1, (0, 0, width, height), width=lineweight)

        else:
            #point entity
            sprite_surface = pygame.Surface((lineweight, lineweight))
            sprite_surface.fill(color2)

        c = e.grant(rack.c("sprite"))
        c.surface = sprite_surface
    else:
        assert hasattr(e.components["sprite"], 'surface')

def render(e):

    PyG.screen.blit(sprite, pos)
