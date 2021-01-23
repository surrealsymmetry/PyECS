import pygame_instance_object as g
import ECS_Inspector as tools

game = g.Game()


def nudge_timer(e):
    c = e.components["timer"]
    c.delta = game.clock.tick(60)
    c.total += (c.delta / 1000)




