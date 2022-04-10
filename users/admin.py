from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(User)
# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
#     list_filter = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
#     # fieldsets = (
#     #     (None, {'fields': ('email', 'password')}),
#     #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     # )
#     # add_fieldsets = (
#     #     (None, {
#     #         'classes': ('wide',),
#     #         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#     #      ),
#     # )
#     search_fields = ['email']
#     ordering = ['email']
