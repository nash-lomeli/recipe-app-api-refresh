from rest_framework import serializers
from drc.apps.profiles.serializers import ShortProfileSerializer

from . import models


class CookedListSerializer(serializers.ModelSerializer):
    user = ShortProfileSerializer(read_only=True)


    class Meta:
        model = models.CookedRecipe
        fields = (
            'id','recipe_id','user',
            'created_at','updated_at',
        )
