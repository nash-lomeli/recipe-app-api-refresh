from rest_framework import serializers
from drc.apps.profiles.serializers import ShortProfileSerializer

from . import models


class LikeListSerializer(serializers.ModelSerializer):
    user = ShortProfileSerializer(read_only=True)


    class Meta:
        model = models.Like
        fields = (
            'id','recipe_id','user_id',
            'created_at','updated_at','user'
        )
