from django.db import models
from drc.apps.core.models import TimestampedModel


class NoteRecipe(TimestampedModel):
    body = models.TextField(blank=True, null=True)

    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='note_recipe',
    )

    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='note_recipe',
    )

    def __str__(self):
        return f'{self.user} wrote {self.body}'
