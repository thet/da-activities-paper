import activities.metamodel as mm

model = mm.Package('testmodel')
model['activities.runtime.testexecutions'] = mm.Profile()
model['main'] = mm.Activity()
act = model['main']

act['pc1'] = mm.PreConstraint(\
    specification='test is not None')

act['start'] = mm.InitialNode()

act['action1'] = mm.OpaqueAction()
act['action1']['execution1'] = mm.Stereotype(profile=profile)
act['action1']['execution1']['foo'] =\
    mm.TaggedValue(value="bar")

act['decision'] = mm.DecisionNode()

act['flow end'] = mm.FlowFinalNode()
act['end'] = mm.ActivityFinalNode()

act['1'] = mm.ActivityEdge(source=act['start'],\
                           target=act['action1'])
act['2'] = mm.ActivityEdge(source=act['action1'],\
                           target=act['decision'])
act['3'] = mm.ActivityEdge(source=act['decision'],\
                           target=act['end'],\
                           guard="test is True")
act['4'] = mm.ActivityEdge(source=act['decision'],\
                           target=act['flow end'],\
                           guard="else")

mm.validate(model)
