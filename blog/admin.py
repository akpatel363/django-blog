from django.contrib import admin
from .models import Post, Comment


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', )
    list_editable = ('status', )
    date_hierarchy = 'publish'
    ordering = ('status', '-publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'created', 'active')
    ordering = ('-created',)
    list_filter = ('name', 'post')
    search_fields = ('body', 'name')
    list_editable = ('active',)
    list_display_links = ('name', 'post')