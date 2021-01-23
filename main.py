import s_def as s
import ECS
import pygame_instance_object as g
import ECS_tests as tests

r = ECS.Rack()

tests.blueprinting(r)
tests.printing_and_sorting(r)
tests.inspector(r)
tests.ecs_systems(r)  # !! breaks other pygame tests !!
tests.pygame_systems(r)

game = g.Game()
r.s("Timer System", "timer", s.nudge_timer)
game.run()

print("end of main")