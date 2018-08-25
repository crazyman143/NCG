from django.contrib import admin

# here we are importing other classes needed to modify the admin tool:
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# we import our custom Profile model that has a one-to-one relationship
# with the built-in user model
from .models import Profile


# Build custom profile class that stacks the profile with the user, then 
# unregisters the default and loads this one in the admin tool:
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# register the Profile class in the admin
admin.site.register(Profile)