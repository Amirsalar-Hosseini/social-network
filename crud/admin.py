from django.contrib import admin
from crud.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'created')
    search_fields = ('slug',)
    list_filter = ('created', 'user')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body'[:10], 'created', 'is_reply')
    search_fields = ('body',)
    list_filter = ('created', 'post', 'user', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')