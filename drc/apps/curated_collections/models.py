from django.db import models
from django.conf import settings

from drc.apps.core.models import TimestampedModel


class CuratedCollection(TimestampedModel):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField()
    collectionRecipes = models.ManyToManyField(	
        'recipes.Recipe',
        related_name='curated_collection',	
        blank=True,
        symmetrical=False,
        through='curated_collections.CollectionRecipe'	
    )

    def __str__(self):
        return self.title


class CollectionRecipe(TimestampedModel):
    display_order = models.IntegerField()
    curatedCollection = models.ForeignKey(
        'curated_collections.CuratedCollection',
        on_delete=models.CASCADE,
        related_name='collection_recipe'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='collection_recipe'
    )

    def __str__(self):
        return f'{self.curatedCollection}: {self.recipe}'
    