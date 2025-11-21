from django.contrib import admin
from .models import *

# Register models
admin.site.register(Client)
admin.site.register(Trainer)
admin.site.register(MembershipType)
admin.site.register(ClientMembership)
admin.site.register(WorkoutType)
admin.site.register(WorkoutClass)
admin.site.register(ClassRegistration)
admin.site.register(Visit)
admin.site.register(Payment)
