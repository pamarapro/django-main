from rest_framework import serializers

from .models import Policy

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = (
            "id",
            "title",
            "short_description",
            "description",
            "get_absolute_url",
            "image",
            "date_added",
            "visible",
            "sort",
        )
