from django.db import models
from django.conf import settings

SITE_URL = settings.SITE_URL
# Create your models here.
class Data(models.Model):
    identity = models.CharField(max_length=200, blank=True, null=True, help_text="Nhập thông tin tên website tối đa 60 ký tự")
    content = models.TextField(blank=True, null=True, help_text="Nhập thông tin tên website tối đa 155 ký tự")

    logo = models.ImageField(upload_to="uploads/site", blank=True, null=True)
    favicon = models.ImageField(upload_to="uploads/site", blank=True, null=True)
    services = models.TextField(blank=True, null=True)

    header_script = models.TextField(blank=True, null=True)
    body_script = models.TextField(blank=True, null=True)
    css_script = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    hotline = models.CharField(max_length=100, blank=True, null=True)
    zalo = models.CharField(max_length=100, blank=True, null=True)
    zalo_oaid = models.CharField(max_length=100, blank=True, null=True)

    google = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    map_iframe = models.TextField(blank=True, null=True, help_text="Thêm iframe map với kích thước width=100%, heigh=300")
    header_text = models.TextField(blank=True, null=True)
    footer_content = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = 'Thông tin công ty'
        verbose_name_plural = "Thông tin công ty"

    def __str__(self):
        return self.identity
    def get_logo(self):
        if self.logo:
            return SITE_URL + self.logo.url
        return ''
# class VariationManager(models.Manager):
#     def address(self):
#         return super(VariationManager, self).filter(variation_category='address', is_active=True)
#     def hotline(self):
#         return super(VariationManager, self).filter(variation_category='hotline', is_active=True)

# variation_category_choices = (
#     ('address', 'address'),
#     ('hotline', 'hotline')
# )

# class Variation(models.Model):
#     address = models.ForeignKey(Data, on_delete=models.CASCADE)
#     variation_address = models.CharField(max_length=100, choices=variation_category_choices)
#     variation_value = models.CharField(max_length=100)
  
#     objects = VariationManager()

#     def __str__(self):
#         return self.variation_value

