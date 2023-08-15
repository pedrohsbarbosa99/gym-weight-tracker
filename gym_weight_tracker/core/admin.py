from django.contrib import admin

from gym_weight_tracker.account.models import User
from gym_weight_tracker.core.models import Exercise, Progression

admin.site.register(Exercise)
admin.site.register(Progression)
admin.site.register(User)
