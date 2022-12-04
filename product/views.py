from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, CategoryListSerializer
from rest_framework import generics, mixins, serializers
from rest_framework_recursive.fields import RecursiveField
from rest_framework.serializers import ModelSerializer


class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:10]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)




class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategorySubSerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        depth = 1
        model = Category
        fields = ("name","id","get_absolute_url","get_image","image", "subcategory", 'get_banner',
        'visibleHomepage', "products",
)

    def get_subcategory(self, obj):
        return CategorySubSerializer(obj.get_children(),many=True).data

class CategoryList(generics.ListAPIView):

    children = RecursiveField(many=True)
    serializer_class = CategorySubSerializer
    queryset = Category.objects.filter(level=0)
    class Meta:
        model = Category
        fields = ('id', 'name', 'children', "get_absolute_url", 'get_banner', 'visibleHomepage')


class ProductDetail(generics.ListAPIView):
    gallery = serializers.SerializerMethodField()
    children = RecursiveField(many=True)
    serializer_class = ProductSerializer
    # queryset = Product.objects.filter(level=0)
    class Meta:
        depth = 1
        model = Product
        fields = ("name",'category',"id","get_absolute_url","get_image","image", "gallery",)

    def get_object(self, product_slug):
        try:
            return Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, product_slug, format=None):
        product = self.get_object(product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySubSerializer(category)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__unaccent__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
