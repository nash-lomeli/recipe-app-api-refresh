from django.db import models
from django.conf import settings

from drc.apps.core.models import TimestampedModel
# from drc.apps.core.utils import recipe_image_file_path


# class RecipeImage(TimestampedModel):
#     image = models.ImageField(null=True,
#         upload_to=recipe_image_file_path,
#         height_field="height_field",
#         width_field="width_field",
#     )
#     height_field = models.IntegerField(default=0)
#     width_field = models.IntegerField(default=0)
#     recipe = models.ForeignKey(
#         'recipes.Recipe',
#         on_delete=models.CASCADE,
#         related_name='recipe_image',
#     )

#     def __str__(self):
#         return self.image


# class InstructionImage(TimestampedModel):
#     image = models.ImageField(null=True,
#         upload_to=recipe_image_file_path,
#         height_field="height_field",
#         width_field="width_field",
#     )
#     height_field = models.IntegerField(default=0)
#     width_field = models.IntegerField(default=0)
#     instruction = models.ForeignKey(
#         'recipes.Instruction',
#         on_delete=models.CASCADE,
#         related_name='instruction_image',
#     )

#     def __str__(self):
#         return self.image


class InstructionIngredient(TimestampedModel):
    body = models.CharField(max_length=255)

    instruction = models.ForeignKey(
        'recipes.Instruction',
        on_delete=models.CASCADE,
        related_name='instruction_ingredient',
    )

    def __str__(self):
        return self.body


class Recipe(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    total_time = models.IntegerField()
    servings = models.IntegerField()
    cuisine = models.CharField(max_length=255, blank=True, null=True)
    is_purchasable = models.BooleanField(default=False)

    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    def __str__(self):
        return self.title
    
    # def ingredient_count(self):
    #     return Ingredient.objects.filter(item__recipe_id=self).count()
    
    # def like_count(self):
    #     return self.like.count()


class Instruction(TimestampedModel):
    body = models.TextField()
    display_order = models.IntegerField()

    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='instructions',
    )

    # completed = models.ManyToManyField(
    #     'profiles.Profile',	
    #     related_name='completed_by',	
    #     blank=True,
    #     symmetrical=False,
    #     through='completed_instructions.CompletedInstruction'
    # )

    def __str__(self):
        return self.body


class Item(TimestampedModel):
    name = models.CharField(max_length=255)
    display_order = models.IntegerField()

    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='items',
    )

    def __str__(self):
        return self.name


class Ingredient(TimestampedModel):
    name = models.CharField(max_length=255)
    display_order = models.IntegerField()

    item = models.ForeignKey(
        'recipes.Item',
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    def __str__(self):
        return self.name
