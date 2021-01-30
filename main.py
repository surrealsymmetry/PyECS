
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


rack.s("Global Time System", "pygame_global_timer", s.pygame_global_timer)
rack.s("Lifespan Countdown", "timer_countdown", s.timer_countdown)
rack.s("Particle Spawner System", "particle_source", "position", s.point_dot_source)
rack.s("Render System", "position", "sprite", s.render)


e_map = rack.e()
e_map.grant(rack.c("position", 50, 100))
e_map.grant(rack.c("box", 200, 200))
e_map.grant(rack.c("sprite"))

e_spawner = rack.e()
e_spawner.grant(rack.c("particle_source", rate=((1/(10 * 100))), max=0))
e_spawner.grant(rack.c("timer_countdown"))
e_spawner.grant(rack.c("position",
                       e_map.components["position"].x + (e_map.components["box"].x/2),
                       e_map.components["position"].y + (e_map.components["box"].y/2)))

PyG.run()
for i in rack.entities:
    tools.inspect(rack.entities[i])
for i in rack.systems:
    tools.inspect(rack.systems[i])
print("end of main")