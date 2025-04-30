from django.contrib import admin
from unfold import admin as u_admin
from apps.users.models import User


@admin.register(User)
class UserAdmin(u_admin.ModelAdmin):
    list_display = ('name','number','age','city','arrived','hobbies','is_staff','is_active')