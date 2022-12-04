from rest_framework import serializers, generics

from .models import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            "id",
            "get_banner",
            'banner',
            'name',
            'description',
            'link',
            "banner_size",
            "running"
        )