from django.contrib import admin
from .models import Post, Tag, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'pub_date', 'modified_time', 'category', 'author',
                    'views', 'status'
                    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
