from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify

from django.conf import settings
SITE_URL = settings.SITE_URL
# from tinymce.models import HTMLField
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    total_spent = models.FloatField(max_length=100)
    max_code = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Mã khuyến mãi'
        verbose_name_plural = "Mã khuyến mãi"

class Promotion(models.Model):
    SIZES = (
    ("banner", "Banner trang chủ: 1920x520 px"),
    ("home1", "Ảnh trang chủ nhỏ 1: 270x340 px"),
    ("home3", "Ảnh trang chủ nhỏ 2: 270x340 px"),

    ("home2", "Ảnh trang chủ lớn giữa: 565x340 px"),
    ("promotion", "Ảnh ngang promotion: 1920x400 px"),

 
)

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    banner = models.ImageField(upload_to="promotion")
    banner_size = models.CharField(max_length=9,
                  choices=SIZES,
                  default="banner", null=True, blank=True)
    running = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Promotion, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Banner chương trình'
        verbose_name_plural = "Banner chương trình"

    def get_banner(self):
        if self.banner:
            return SITE_URL + self.banner.url
        return ''

