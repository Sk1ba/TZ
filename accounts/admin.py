from django.contrib import admin
from .models import User, Role, Resurs, AccessLvl, UserRole

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Resurs)
admin.site.register(AccessLvl)
admin.site.register(UserRole)