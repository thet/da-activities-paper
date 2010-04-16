import activities.metamodel as mm

class Patient(object):
    def __init__(self, name, health):
        self.name = name
        self.health = health # int btw. 0 (dead) and 100 (healthy)

profile = mm.Profile('activities.test.hospital')

model = mm.Package('hospital-admission')
model[profile.__name__] = profile
model['main'] = mm.Activity()
act = model['main']

act['pc1'] = mm.PreConstraint(specification='patient is not None')
act['pc2'] = mm.PreConstraint(specification='patient.health > 0')
act['po1'] = mm.PostConstraint(specification='patient.health >= 90')

act['start'] = mm.InitialNode()
act['d1'] = mm.DecisionNode()
act['m1'] = mm.MergeNode()
act['f1'] = mm.ForkNode()
act['j1'] = mm.JoinNode()
act['end'] = mm.ActivityFinalNode()

act['first diagnosis'] = mm.OpaqueAction()
act['first diagnosis']['diagnosis'] = mm.Stereotype(profile=profile)

act['acute therapy'] = mm.OpaqueAction()
act['acute therapy']['therapy'] =\
    mm.Stereotype(profile=profile)
act['acute therapy']['therapy']['variation'] =\
    mm.TaggedValue(value="acute")

act['data acquisition'] = mm.OpaqueAction()
act['data acquisition']['data-acquisition'] =\
    mm.Stereotype(profile=profile)

act['data verification'] = mm.OpaqueAction()
act['data verification']['data-verification'] =\
    mm.Stereotype(profile=profile)

act['diagnosis'] = mm.OpaqueAction()
act['diagnosis']['diagnosis'] =\
    mm.Stereotype(profile=profile)

act['normal therapy'] = mm.OpaqueAction()
act['normal therapy']['therapy'] =\
    mm.Stereotype(profile=profile)
act['normal therapy']['therapy']['variation'] =\
    mm.TaggedValue(value="normal")


act['1'] = mm.ActivityEdge(\
    source=act['start'],\
    target=act['first diagnosis'])
act['2'] = mm.ActivityEdge(\
    source=act['first diagnosis'],\
    target=act['d1'])
act['3'] = mm.ActivityEdge(\
    source=act['d1'],\
    target=act['acute therapy'],
    guard="diagnosis == 'acute'")
act['4'] = mm.ActivityEdge(\
    source=act['d1'],\
    target=act['m1'],
    guard="diagnosis == 'normal'")
act['5'] = mm.ActivityEdge(\
    source=act['acute therapy'],\
    target=act['m1'])
act['6'] = mm.ActivityEdge(\
    source=act['m1'],\
    target=act['data acquisition'])
act['7'] = mm.ActivityEdge(\
    source=act['data acquisition'],\
    target=act['f1'])
act['8'] = mm.ActivityEdge(\
    source=act['f1'],\
    target=act['data verification'])
act['9'] = mm.ActivityEdge(\
    source=act['f1'],\
    target=act['diagnosis'])
act['10'] = mm.ActivityEdge(\
    source=act['data verification'],\
    target=act['j1'])
act['11'] = mm.ActivityEdge(\
    source=act['diagnosis'],\
    target=act['j1'])
act['12'] = mm.ActivityEdge(\
    source=act['j1'],\
    target=act['normal therapy'])
act['13'] = mm.ActivityEdge(\
    source=act['normal therapy'],\
    target=act['end'])

mm.validate(model)
