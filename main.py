import s_def as s
import ECS
import PyG
import ECS_tests as tests

r = ECS.Rack()

tests.blueprinting(r)
tests.printing_and_sorting(r)
tests.inspector(r)
tests.ecs_systems(r)  # !! breaks other pygame tests !!
tests.pygame_systems(r)

r.s("Timer System", "timer", s.nudge_timer)

print("end of main")