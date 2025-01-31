from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('slug', 'published_at')
    actions_on_top = True
    actions_selection_counter = True


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(AuthorProfile)
