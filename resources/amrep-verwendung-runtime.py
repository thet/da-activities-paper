from activities.runtime.runtime import ActivityRuntime
ar = ActivityRuntime(model['main'])

ar.start(data={'test':False})

# Print Tokenstate e.g.
# "1: ...Token..., data: {'test': False}"
ar.ts()

ar.next()

# Restart of runtime
activity = ar.activity
token_pool = ar.token_pool

del ar

new_ar = ActivityRuntime(activity)
new_ar.token_pool = token_pool

new_ar.next()

# Changing the model at runtime
new_ar.activity['action1']['execution1']['foo'].value =\
    "Changed at runtime!"

import activities.metamodel as mm
mm.validate(new_ar.activity)

new_ar.stop()
