from django.contrib import admin
from crud.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'created')
    search_fields = ('slug',)
    list_filter = ('created', 'user')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)