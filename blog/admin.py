from django.contrib import admin
from .models import Users, Signup, BlogPost, BlogComment, Article, ArticleComment, Que, QueAns
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Users)
admin.site.register(Signup)
admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(Article)
admin.site.register(ArticleComment)
admin.site.register(Que)
admin.site.register(QueAns)

#admin.site.register(User)