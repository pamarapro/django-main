from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    author = serializers.ReadOnlyField(source='author.name',)
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "category",
            "get_image",
            'get_absolute_url',
            "get_thumbnail",
            "slug",
            "short_des",
            "content",
            "posted_date",
            "image",
            "author",
            "status"
        )