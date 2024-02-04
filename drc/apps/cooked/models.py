from django.db import models
from drc.apps.core.models import TimestampedModel


class CookedRecipe(TimestampedModel):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='cooked_recipe'
    )

    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='cooked_recipe'
    )

    def __str__(self):
        return f'{self.user} cooked {self.recipe}'
