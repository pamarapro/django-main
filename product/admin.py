from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from product.models import Category, Product, ProductImages, Brand, ProductGallery, Variation, ProductAttribute, ReviewRating
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'slug',
        'image',
        # ...more fields if you feel like it...    
    ),
    list_display_links=(
        'indented_title',
    ),
)


# @admin_thumbnails.thumbnail('image')  
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1 

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    inlines = [ProductGalleryInline, VariationInline, ProductAttributeInline]
    list_display=(
        # 'img',
        # 'image_tag',
        'name',
        'price',
        'discount_price',
        'sku',
        'brand',
        'stock',
        
        )
    editable_fields = ('price',),
    fields=('name','slug', 'category', 'description','brand', 'price', 'discount_price','image', 'sku','stock', 'label', 'is_available')



class BrandAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display=(
        'img',
        'name',
      
        
        )
    # readonly_fields = ('name',),
    # fields=('name','slug', 'category', 'description','brand', 'price',('discount_percentage', 'discount_price'),'image', ('sku','stock'), 'label', 'is_available')


# admin.site.register(Product,
#  list_display=(
#         'img',

#         'name',

#         'category',
#         'price',
#         'discount_price',
        
#         ),
#     editable_fields = ('price',),
#     readonly_fields = ['img'],
#     fields=('name','slug', 'category', 'description','brand', 'price',('discount_percentage', 'discount_price'),'image','img', ('sku','stock'), 'label', 'is_available')

# )

admin.site.register(Product,ProductAdmin)

admin.site.register(Brand, BrandAdmin)

admin.site.register(ReviewRating)
