from rest_framework import serializers

from . import models

from drc.apps.recipes import models as recipe_models
from drc.apps.profiles import models as profile_models

class RecipeImageSerializer(serializers.ModelSerializer):


    class Meta:
        model = recipe_models.RecipeImage
        fields = (
            'id','image'
        )
        read_only_fields = ('id','image',)


class ShortProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')


    class Meta:
        model = profile_models.Profile
        fields = (
            'id','username',
        )
        read_only_fields = ('id','username',)


class RecipeSerializer(serializers.ModelSerializer):
    RecipeImage = RecipeImageSerializer(many=True, read_only=True, source='recipe_image')
    author = ShortProfileSerializer(read_only=True)
    has_like = serializers.SerializerMethodField(read_only=True, required=False)
    like_count = serializers.SerializerMethodField(read_only=True, required=False)


    class Meta:
        model = recipe_models.Recipe
        fields = (
            'id','title','author','total_time','servings',
            'slug','has_like','like_count','RecipeImage',
        )
        read_only_fields = ('id','title','author','total_time','servings',
            'slug','has_like','like_count','RecipeImage',
        )

    def get_has_like(self, obj):
        request = self.context.get('request', None)

        if request is None:
            return False

        if request.user.is_authenticated == False:
            return False
        
        recipe = obj

        return request.user.profile.has_like(recipe)

    def get_like_count(self, obj):
        likes = self.context.get('likes', None)

        if likes is None:
            return None

        result = dict((k, likes[k]) for k in [obj.id] if k in likes) 

        return result[obj.id]


class CollectionRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)


    class Meta:
        model = models.CollectionRecipe
        fields = (
            'id','created_at','updated_at','display_order','recipe',
        )
        read_only_fields = ('id','created_at','updated_at','recipe',)

    def create(self, validated_data):
        recipe = self.context.get('recipe')
        curated_collection = self.context.get('curated_collection')

        return models.CollectionRecipe.objects.create(
            recipe=recipe,
            curatedCollection=curated_collection, 
            **validated_data,
        )


class CuratedCollectionSerializer(serializers.ModelSerializer):
    # one needs to mention the related name of the joined model starting from the Meta Model.
    # if a field name change is requried away from the related name, user 'source' to target related name
    # EX:  
    # test = CollectionRecipeListSerializer(many=True, read_only=True, source='collection_recipe')
    collection_recipe = CollectionRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = models.CuratedCollection
        fields = (
            'id','title', 'subtitle','display_order','collection_recipe',
        )
        read_only_fields = ('id','collection_recipe',)
