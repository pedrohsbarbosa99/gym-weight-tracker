from django.contrib import admin

from gym_weight_tracker.account.models import User
from gym_weight_tracker.core.models import (
    Exercise,
    Progression,
    Routine,
    RoutineExercise,
    RoutineExerciseExecution,
)

admin.site.register(Exercise)
admin.site.register(Routine)
admin.site.register(RoutineExercise)
admin.site.register(RoutineExerciseExecution)
admin.site.register(Progression)
admin.site.register(User)
