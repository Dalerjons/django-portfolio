from django.contrib import admin
from .models import Category, Cinema, Comment, Profile

# Register your models here.
@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'category', 'views', 'created_at']
    list_display_links = ['pk', 'title']
    list_filter = ['category']




admin.site.register(Category)
# admin.site.register(Cinema)
admin.site.register(Comment)
admin.site.register(Profile)