from rest_framework import serializers
from . import models

class NoteRecipeSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.NoteRecipe
        fields = (
            'id','body','recipe_id','user_id',
            'created_at','updated_at',
        )

    def create(self, validated_data):
        user = self.context.get('user')
        recipe = self.context.get('recipe')

        return models.NoteRecipe.objects.create(user=user, recipe=recipe, **validated_data)

class ShortNoteRecipeSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.NoteRecipe
        fields = (
            'id','body','updated_at',
        )