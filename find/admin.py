from django.contrib import admin
from .models import Post_type, Post, Relative, Missing_person, Victim, Comment

class CommentInline(admin.TabularInline):
	model = Comment

class PostAdmin(admin.ModelAdmin):
	#list_display = "__all__"
	list_filter = ['time']
	serach_fields = ['id']
	inlines = [CommentInline]


admin.site.register(Post_type)
admin.site.register(Post, PostAdmin)
admin.site.register(Relative)
admin.site.register(Missing_person)
admin.site.register(Victim)

