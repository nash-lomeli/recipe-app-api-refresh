from rest_framework import serializers	
from drc.apps.recipes import models as recipe_models	
from . import models	

class ShortSavedRecipeSerializer(serializers.ModelSerializer):	


    class Meta:	
        model = recipe_models.Recipe	
        fields = (	
            'id','title',
        )


class SaveRecipeSerializer(serializers.ModelSerializer):	

    recipe = ShortSavedRecipeSerializer()	


    class Meta:	
        model = models.SaveRecipe	
        fields = (	
            'id','recipe','created_at','updated_at'	
        )