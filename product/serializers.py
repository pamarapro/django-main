from rest_framework import serializers

from .models import Category, Product, ProductGallery

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery

        fields = ("id", 'get_image',)
        # depth = 1
    def create(self):
        return ProductGallery.objects.create({"id": 0, "get_image": "url"})

class CategoryProductSerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            'tree_id',
            'parent_id',
            'level',
            "name",
            "get_absolute_url",
            "products",
            'get_banner',
        )

class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source='brand.name')
    gallery = ProductImageSerializer(many=True)
    category = CategoryProductSerializer(many=True)
    # category = serializers.ReadOnlyField(source='category.name',)
    class Meta:
        model = Product
        fields = ('id', 'category','name','brand', 'gallery', 'sku','get_absolute_url',
        'description', 'price', 'discount_price', 'discount_percentage','get_price', 'stock', 'label','image', 'get_image',
        'is_available', 'get_thumbnail',)
 

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            'tree_id',
            'parent_id',
            'level',
            "name",
            "get_absolute_url",
            'get_banner',
            "get_children",
            "products",

            
        )

class CategoryListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = (
            'id',
            'tree_id',
            'parent_id',
            'level',
            'get_image',
            'name',
            'slug',
            "get_absolute_url",
            'get_banner',

        )


