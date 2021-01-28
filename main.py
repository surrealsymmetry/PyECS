
import s_def as s
import rack
import ECS_Inspector as tools
import PyG
#import ECS_tests as tests

#tests.blueprinting()
#tests.printing_and_sorting()
#tests.inspector()
#tests.ecs_systems()  # !! breaks other pygame tests !!
#tests.pygame_systems()


rack.s("Timer System", "timer", s.nudge_timer)
rack.s("Render System", "position", "visible", s.prep_sprites, s.render)


e_map = rack.e()
e_map.grant(rack.c("position", 50, 100))
e_map.grant(rack.c("bounds", 200, 200))
e_map.grant(rack.c("visible"))

PyG.run()

print("end of main")