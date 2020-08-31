from django.contrib import admin
from .models import Post
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    # list_display = ['title','made', 'updated']
    # list_display_links = ['made']
    # list_filter = ['updated', 'title']
    # list_editable = ['title']
    # search_fields = ['content']
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)