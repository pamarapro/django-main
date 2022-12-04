from rest_framework import serializers

from .models import Data

class DataSerializer(serializers.ModelSerializer):
  class Meta:
        model = Data
        fields = (
            "id",
            "identity",
            "content",
            "logo",
            'get_logo',
            'favicon',
            "services",
            "header_script",
            "body_script",
            "css_script",
            "website",
            "email",
            "facebook",
            "zalo",
            "zalo_oaid",
            "google",
            "instagram",
            "map_iframe",
            "header_text",
            'footer_content',
        )