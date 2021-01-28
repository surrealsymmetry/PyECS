import rack
import PyG
import pygame
import ECS_Inspector as tools

def nudge_timer(e):
    c = e.components["timer"]
    c.delta = PyG.clock.tick(60)
    c.total += (c.delta / 1000)

__surface_lookup = {} # used by prep_sprites and render
def prep_sprites(e):
    color1 = (180, 255, 200)
    color2 = (255, 180, 200)
    lineweight = 3

    if 'bounds' in e.components:
        #box entity
        width, height = e.components["bounds"].x, e.components["bounds"].y
        sprite_surface = pygame.Surface((width, height))
        sprite_surface.set_colorkey((0,0,0))
        pygame.draw.rect(sprite_surface, color1, (0, 0, width, height), width=lineweight)
        sprite_surface = sprite_surface.convert_alpha()

    else:
        #point entity
        sprite_surface = pygame.Surface((lineweight, lineweight))
        sprite_surface.fill(color2)
    # components should be pure data, no oop method objects
    # todo figure out how to get pngs in here
    #c = e.grant(rack.c("sprite"))
    #c.surface = sprite_surface
    __surface_lookup.update({e.id:sprite_surface})


def render(e):
    pos = e.components["position"].x, e.components["position"].y
    PyG.screen.blit(__surface_lookup[e.id], pos)
