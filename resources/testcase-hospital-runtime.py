Model- and Runtime Import and Instantiation of the Runtime
==========================================================
    >>> from activities.test.hospital.model import model, Patient
    >>> from activities.runtime.runtime import ActivityRuntime
    >>> ar = ActivityRuntime(model['main'])

Testing very high disease
=========================
    >>> ar.start({'patient':Patient("Mister Patient", 10)})
    >>> ar.ts()
    1: <...Token...>, data: {'patient': <...Patient...>}

    >>> ar.next()
    'executing: "first diagnosis"'
    >>> ar.ts()
    2: ... data: {'patient': <...Patient...>, 'diagnosis': 'acute'}

    >>> ar.next()
    >>> ar.ts()
    3: ...

    >>> ar.next()
    'executing: "acute therapy"'
    >>> ar.ts()
    5: ...

    >>> ar.next()
    >>> ar.ts()
    6: ...

    >>> ar.next()
    'executing: "data acquisition"'
    >>> ar.ts()
    7: ... data: {'patient': <...Patient...>, 'name': 'Mister Patient', 'diagnosis': 'acute'}

    >>> ar.next()
    >>> ar.ts()
    8: ...
    9: ...

    >>> ar.next()
    'executing: "data verification"'
    'executing: "diagnosis"'
    >>> ar.ts()
    10: ... data: {'patient': <...Patient...>, 'name': 'Mister Patient'}
    11: ... data: {'patient': <...Patient...>, 'name': 'Mister Patient', 'diagnosis': 'normal'}

    >>> ar.next()
    >>> ar.ts()
    12: ... data: {'patient': <...Patient...>, 'name': 'Mister Patient', 'diagnosis': 'normal'}

    >>> ar.next()
    'executing: "normal therapy"'

We are short before the end of the graph
    >>> ar.ts()
    13: ...

Let's check our patient's health
    >>> ar.token_pool[0].data['patient'].health
    80


Thats way too less! Our patient is not healthy enough
but our model is not prepared for this case.
We have to change our model at runtime
with active tokens in place!


Changing the model at runtime
=============================
We have access to the activity stored in the runtime engine.
    >>> ar.activity
    <Activity ...>

Let's add an DecisionNode to redirect the token to
"normal therapy" if health < 90
    >>> from activities.metamodel.elements import DecisionNode
    >>> from activities.metamodel.elements import MergeNode
    >>> from activities.metamodel.elements import ActivityEdge
    >>> ar.activity['d2'] = DecisionNode()
    >>> ar.activity['m2'] = MergeNode()
    >>> ar.activity['12'].target = ar.activity['m2']
    >>> ar.activity['13'].target = ar.activity['d2']
    >>> ar.activity['14'] = ActivityEdge(\
    ...     source=ar.activity['m2'],\
    ...     target=ar.activity['normal therapy'])
    >>> ar.activity['15'] = ActivityEdge(\
    ...     source=ar.activity['d2'],\
    ...     target=ar.activity['m2'],\
    ...     guard="patient.health < 90")
    >>> ar.activity['16'] = ActivityEdge(
    ...     source=ar.activity['d2'],\
    ...     target=ar.activity['end'],\
    ...     guard="patient.health >= 90")
    >>> from activities.metamodel.elements import validate
    >>> validate(ar.activity)


Our token state didn't change
    >>> ar.ts()
    13: ...

Going back to MergeNode "m2"
    >>> ar.next()
    >>> ar.ts()
    15: ...

    >>> ar.next()
    >>> ar.ts()
    14: ...

    >>> ar.next()
    'executing: "normal therapy"'
    >>> ar.ts()
    13: ...

    >>> ar.next()
    >>> ar.ts()
    16: ...

    >>> ar.token_pool[0].data['patient'].health
    120


Testing Postconditions
======================
There is one more thing untested: Postcondition checks.

Unluckily, our patient died...
    >>> ar.token_pool[0].data['patient'].health = 0

And our postcondition cannot be fulfilled...
    >>> ar.next()
    Traceback (most recent call last):
    ...
    ActivityRuntimeError: PostConstraint not fulfilled: "patient.health >= 90"
