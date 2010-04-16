XMI to Activities Transform
===========================
Lookup transform and read source and target
  >>> from agx.core.interfaces import ITransform
  >>> from zope.component import getUtility
  >>> transform = getUtility(ITransform, name="xmi2act")

Import handler to register them.
  >>> from activities.transform.xmi import handler

  >>> import os
  >>> sourcepath = os.path.join(\
  ...     os.path.dirname(__file__),\
  ...     'data', 'activities-testmodel.uml')

  >>> xml = transform.source(sourcepath)
  >>> xml
  <XMLNode object ...>

  >>> from agx.core import Processor
  >>> processor = Processor('xmi2act')
  >>> pkg = processor(xml, transform.target())
  >>> from activities.metamodel.elements import validate
  >>> validate(pkg)

  >>> act = pkg.activities[0]
  >>> act
  <Activity...>

  >>> act.actions
  [<... 'action1' ... 'action2' ... 'action3' ...>]

  >>> act.nodes
  [<... 'action1' ... 'action2' ... 'action3' ... 'initial node' ... 'activity final node' ... 'flow final node' ... 'fork node' ... 'merge node' ... 'join node' ... 'decision node' ...>]

  >>> act.edges
  [<...'1' ...'2' ...'3' ...'7' ...'5' ...'10' ...'11' ...'6' ...'9' ...'8' ...'4' ...>]
