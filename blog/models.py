from django.db import models
# Create your models here.
from django.conf import settings
SITE_URL = settings.SITE_URL
from io import BytesIO
from PIL import Image
from django.core.files import File

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Chuyên mục'
        verbose_name_plural = "Chuyên mục"

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(upload_to='blog_media/author/', null=True)
    description =  models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, null=True)
    class Meta:
        verbose_name = 'Tác giả'
        verbose_name_plural = "Tác giả"

    def __str__(self):
        return self.name

class Post(models.Model):
    options = (
        ('nhap', 'Lưu nháp'),
        ('dang', 'Đăng bài'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, help_text="Không nhập quá 70 ký tự")
    slug = models.SlugField(max_length=250, null=True)
    short_des =  models.TextField(blank=True, null=True)
    content =  models.TextField(blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/posts', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, choices=options, default='dang')

    thumbnail = models.ImageField(upload_to='uploads/posts', blank=True, null=True)

    class Meta:
        verbose_name = 'Bài viết'
        verbose_name_plural = "Bài viết"
        # verbose_plural_name = 'Những bài viết'
        ordering = ('-posted_date',)

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return SITE_URL + self.image.url
        return ''
    def get_thumbnail(self):
        if self.thumbnail:
            return SITE_URL + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return SITE_URL + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_absolute_url(self):
        return f'/post/{self.slug}/'
