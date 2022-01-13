from django.contrib import admin
from .models import User,FndF,Post,Like,Comment,Message,online

# Register your models here.

admin.site.register(User)
admin.site.register(FndF)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(online)