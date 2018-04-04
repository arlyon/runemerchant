from rest_framework import serializers

from merchapi.models import Tag
from merchapi.serializers.base import composed_serializer, TagSerializer


@composed_serializer
class TagItemSerializer(serializers.ModelSerializer, TagSerializer):
    """

    """
    class Meta:
        model = Tag
        fields = ('items',)