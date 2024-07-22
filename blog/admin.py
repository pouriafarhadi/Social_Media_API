from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "total_likes", "total_saves"]


admin.site.register(Comment)
