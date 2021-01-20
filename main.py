import ECS
import s_def as s

import ECS_Inspector as tools
import ECS_tests as tests

    ###
    ### Testing ECS, pwint, inspector
    ###

r = ECS.Rack()

#tests.blueprinting(r)
#tests.printing_and_sorting(r)
#tests.inspector(r)
#tests.ecs_systems(r)  # !! breaks other pygame tests !!
#tests.pygame_systems(r)

s.pg_mainloop(r)