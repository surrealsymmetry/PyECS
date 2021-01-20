import pygame
import ECS_Inspector as tools

clock = pygame.time.Clock()

def pg_mainloop(r):
    pygame.init()
    view = pygame.display.set_mode((640, 480))

    bg = pygame.Surface(view.get_size())
    bg.fill((85, 82, 87))
    bg = bg.convert()
    e_bg = r.e()
    e_bg.grant(r.c("graphic", sprite=bg, bounds=bg.get_rect(), layer=-1))

    mainloop = True

    r.s("Timer System", "timer", nudge_timer)

###
###
###

def nudge_timer(e):
    c = e.components["timer"]
    c.delta = clock.tick(60)