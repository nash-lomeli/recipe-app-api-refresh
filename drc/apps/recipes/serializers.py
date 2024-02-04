from rest_framework import serializers
from django.contrib.auth import get_user_model
from drc.apps.profiles.serializers import ShortProfileSerializer

from . import models

# from src.apps.notes import serializers as note_serializers

# class RecipeImageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.RecipeImage
#         fields = ('id','image')
#         read_only_fields = ('id',)
    
#     def create(self, validated_data):
#         recipe = self.context.get('recipe')

#         return models.RecipeImage.objects.create(recipe=recipe, **validated_data)


# class InstructionImageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.InstructionImage
#         fields = ('id','image')
#         read_only_fields = ('id',)

#     def create(self, validated_data):
#         instruction = self.context.get('instruction')

#         return models.InstructionImage.objects.create(instruction=instruction, **validated_data)


class InstructionIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InstructionIngredient
        fields = ('id','body',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        instruction = self.context.get('instruction')

        return models.InstructionIngredient.objects.create(instruction=instruction, **validated_data)

  
class InstructionSerializer(serializers.ModelSerializer):

    # Commenting out InstructionImage until we can provide images at the instruction level
    #InstructionImage = InstructionImageSerializer(many=True, read_only=True, source='instruction_image')
    instruction_ingredients = InstructionIngredientSerializer(many=True, read_only=True, source='instruction_ingredient')
    # is_completed = serializers.SerializerMethodField(read_only=True, required=False)


    class Meta:
        model = models.Instruction
        fields = (
            'id','body','display_order',
            'instruction_ingredients',)
            #'is_completed',
        #)
        read_only_fields = ('id',)#'is_completed',)

    def create(self, validated_data):
        recipe = self.context.get('recipe')
        type(recipe)

        return models.Instruction.objects.create(recipe=recipe, **validated_data)
    
    # def get_is_completed(self, obj):
    #     request = self.context.get('request', None)

    #     if request is None:
    #         return False
        
    #     if request.user.is_authenticated == False:
    #         return False
        
    #     instruction = obj

    #     return request.user.profile.has_completed(instruction)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = (
            'id','name','display_order'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        item = self.context.get('item')

        return models.Ingredient.objects.create(item=item, **validated_data)


class ItemSerializer(serializers.ModelSerializer):

    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = models.Item
        fields = (
            'id','name','display_order','ingredients'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        recipe = self.context.get('recipe')
        
        return models.Item.objects.create(recipe=recipe, **validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    author = ShortProfileSerializer(read_only=True)
    slug = serializers.SlugField(required=False)
    has_like = serializers.SerializerMethodField(read_only=True, required=False)
    # has_cooked = serializers.SerializerMethodField(read_only=True, required=False)
    # recipe_note = serializers.SerializerMethodField(read_only=True, required=False)
    instructions = InstructionSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    # RecipeImage = RecipeImageSerializer(many=True, read_only=True, source='recipe_image')


    class Meta:
        model = models.Recipe
        fields = (
            'id','author','title','description','cuisine',
            'total_time','servings','slug','is_purchasable',
            #'recipe_note',
            'has_like','like_count',
            #'has_cooked',
            'ingredient_count',
            'created_at','updated_at',
            #'RecipeImage',
            'instructions','items',
        )
        read_only_fields = ('id','slug',
            'has_like','like_count',
            #'has_cooked',
            'ingredient_count',
            'created_at','updated_at',
        )


    def create(self, validated_data):
        author = self.context.get('author', None)

        return models.Recipe.objects.create(author=author, **validated_data)
    
    def get_has_like(self, obj):
        request = self.context.get('request', None)

        if request is None:
            return False
        
        if request.user.is_authenticated == False:
            return False
        
        recipe = obj

        return request.user.profile.has_like(recipe)

    # def get_has_cooked(self, obj):
    #     request = self.context.get('request', None)

    #     if request is None:
    #         return False
        
    #     if request.user.is_authenticated == False:
    #         return False
        
    #     recipe = obj

    #     return request.user.profile.has_cooked(recipe)
    
    # def get_recipe_note(self, obj):
    #     request = self.context.get('request', None)

    #     if request is None:
    #         return None
        
    #     if request.user.is_authenticated == False:
    #         return None

    #     recipe = obj

    #     return note_serializers.ShortNoteRecipeSerializer(request.user.profile.recipe_note(recipe)).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    author = ShortProfileSerializer(read_only=True)
    has_like = serializers.SerializerMethodField(read_only=True, required=False)
    like_count = serializers.SerializerMethodField(read_only=True, required=False)
    # RecipeImage = RecipeImageSerializer(many=True, read_only=True, source='recipe_image')

    class Meta:
        model = models.Recipe
        fields = (
             'id','title','total_time','slug','author','has_like','like_count',#,'is_purchasable','RecipeImage',
        )
        read_only_fields = (
             'id','title','total_time','slug','author','has_like','like_count',#,'is_purchasable',,'RecipeImage',
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

    # def get_has_cooked(self, obj):
    #     request = self.context.get('request', None)

    #     if request is None:
    #         return False
        
    #     if request.user.is_authenticated == False:
    #         return False
        
    #     recipe = obj

    #     return request.user.profile.has_cooked(recipe)