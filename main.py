import ECS

r = ECS.Rack()
e = r.request_entity()
c = e.grant(r.request_component("position"))
c2 = r.request_component("position")
c3 = r.request_component("position")
c.data = [25, 40]

print(r)

print("The entities position is x= %s y = %s" % (e.components["position"].data[0],e.components["position"].data[1]))