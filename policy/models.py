from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Policy(models.Model):
    title = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/policy', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)
    sort = models.IntegerField()


    class Meta:
        ordering = ('sort',)
        verbose_name = 'Trang nội dung'
        verbose_name_plural = "Trang nội dung"
      
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/policy/{self.slug}/'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Policy, self).save(*args, **kwargs)

    