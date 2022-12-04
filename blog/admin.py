from django.contrib import admin
from .models import Post, Category, Author
import django.apps
from django import forms 
from django_summernote.admin import SummernoteModelAdmin
# Collect all models
models = django.apps.apps.get_models()
# Register your models here.
TEXT = 'Vui lòng nhập tiêu đề và slug đầy đủ ký tự.'
# class BlogAdmin(admin.AdminSite):
#     site_header = 'Blog Site Area'
#     site_title = 'Blog Admin'
#     index_title = 'Blog'
#     login_template = 'blog/admin/login.html'
#     index_template = 'blog/admin/base.html'
    
# class PostAdmin(admin.ModelAdmin):
#     # fields = ['title','author']
#     fieldsets = (
#         ('SEO', {
#             "fields": (
#                 'title', 'slug',
#             ),
#             'description': '%s' % TEXT,
#         }),
#         ('Bản quyền', {
#             "fields": ('author', 'category',),
#             "classes": ('collapse',),
#         }),
#     )
    

# class PostAdmin(admin.ModelAdmin):
#     class Meta:
#         list_display = ('title', 'slug')

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Nhập đủ ký tự để SEO'

    class Meta:
        model = Post
        exclude = ('',)

class PostFormAdmin(admin.ModelAdmin):
    form = PostForm



# blog_site = BlogAdmin(name='BlogAdmin')
# admin.site.register(Category)
# admin.site.register(Author)


class SummerAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
# myModels = [Post, Category, Author]

admin.site.register(Category)
admin.site.register(Post, SummerAdmin)

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass

# admin.site.unregister(django.contrib.auth.models.Group)