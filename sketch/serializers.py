from rest_framework import serializers
from .models import SketchImage

class SketchImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SketchImage
        fields = "__all__"
