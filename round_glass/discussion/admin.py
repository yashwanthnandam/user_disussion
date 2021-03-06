from django.contrib import admin
from .models import CustomUser,Tags, Discussion
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name','phone_number')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),)


# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tags)
admin.site.register(CustomUser)
admin.site.register(Discussion)
