from django.contrib import admin
from posts.models import Post

# from .models import MarkdownContent
# class MarkdownContentAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ["title"]}
# admin.site.register(MarkdownContent, MarkdownContentAdmin)


# admin.site.register(Category)
admin.site.register(Post)
