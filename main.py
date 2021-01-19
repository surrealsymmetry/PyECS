import ECS
import pygame
import ECS_Inspector as tools
import ECS_tests as tests

    ###
    ### Testing ECS, pwint, inspector
    ###

r = ECS.Rack()

#tests.blueprinting(r)
#tests.printing_and_sorting(r)
tests.inspector(r)
#tests.ecs_systems(r)                    #this fakes a bunch of updates so will cause true pygame updates to fail
tests.pygame_systems(r)

"""
c = r.c("graphic")
tools.inspect(c)
c.bounds = pygame.Rect(0,0,20,20)
tools.inspect(c)

"""