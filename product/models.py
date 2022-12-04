from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import mark_safe

from django.conf import settings
SITE_URL = settings.SITE_URL

class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', default=0)
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/icons', blank=True, null=True, help_text="File PNG, kích thước: 64 x 64 px")
    banner = models.ImageField(upload_to='uploads/banner', blank=True, null=True, help_text="Kích thước tiêu chuẩn banner: 1920 x 520px")
    visibleHomepage = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Danh mục sản phẩm'
        verbose_name_plural = "Danh mục sản phẩm"
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

    def __str__(self):
        return self.name

    def get_children(self):
        return super().get_children()
    
    def get_absolute_url(self):
        return f'/category/{self.slug}/'

    def get_image(self):
        if self.image:
            return self.image.url
        return ''
    def get_banner(self):
        if self.banner:
            return self.banner.url
        return ''

    class MPTTMeta:
        order_insertion_by = ['name']


class Brand(models.Model):
    
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="uploads/brands", blank=True, null=True)
    slug= models.SlugField(blank=True, unique=True, null=True)
    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return ''
    class Meta:
        verbose_name = 'Thương hiệu'
        verbose_name_plural = "Thương hiệu"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    @property
    def img(self): #new
        return mark_safe('<img src = "{url}" height="50" />'.format(
             url = self.image.url
         ))

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products',)
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    sku = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    discount_percentage = models.IntegerField(default=35, null=True)
    discount_price = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=20)
    label = models.CharField(max_length=50, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnail/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def get_price(self):
        if(self.discount_price):
            price = self.discount_price
        else:
            price = self.price
        return price

    class Meta:
        ordering = ('-date_added',)
        verbose_name = 'Sản phẩm'
        verbose_name_plural = "Sản phẩm"

    def averageRating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

      
    @property
    def discount(self):
        product_id = self.id
        variation = Variation.objects.get(id=product_id)
        if variation.price:
            price = variation.price
            return int(price)

        elif self.discount_percentage > 0:
            price = self.price - self.price * self.discount_percentage / 100
            return int(price)
        
        else:
            price = self.price
            return int(price)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=70)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    @property
    def img(self): #new
        return mark_safe('<img src = "{url}" height="50" />'.format(
             url = self.image.url
         ))

    def image_tag(self):
        from django.utils.html import escape
        return escape('<img src={{SITE_URL+self.image.url}}/>')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="uploads/products", default="", null=True, blank=True)


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choices = (
    ('color', 'color'),
    ('size', 'size')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

    class Meta:
        verbose_name = 'Thuộc tính'
        verbose_name_plural = "Thuộc tính"


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    review = models.CharField(max_length=200, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.subject
    class Meta:
        verbose_name = 'Đánh giá'
        verbose_name_plural = "Đánh giá"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="uploads/products", null=True)

    class Meta:
        verbose_name = 'Giá trị thuộc tính'
        verbose_name_plural = "Giá trị thuộc tính"
    def __str__(self):
        return self.product.name

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name="gallery", default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/products', max_length=255)
    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = 'Hình ảnh sản phẩm'
        verbose_name_plural = "Hình ảnh sản phẩm"
    def get_absolute_url(self):
        return f'{self.image.url}'
    def main_image(self):
        if self.product.image:
            return self.product.image.url
    def get_image(self):
        if self.image:
            return self.image.url
        return ''