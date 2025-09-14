from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    
admin.site.register(Book, BookAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

    list_display = ['username', 'email', 'date_of_birth', 'is_staff']


admin.site.register(CustomUser, CustomUserAdmin)