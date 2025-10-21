from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
