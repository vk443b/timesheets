from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Users, ClientUser
from users.forms import UserCreationForm

# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number")

    fields = ("first_name", "last_name", "middle_name", "username", "password", "email", "is_staff", "is_superuser")

    add_form = UserCreationForm

    class meta:
        verbose_name = "Admins"

@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number")

    fields = ("first_name", "last_name", "middle_name", "username", "password", "email")

    add_form = UserCreationForm

    class meta:
        verbose_name = "Users"