from django.db import models
from drc.apps.core.models import TimestampedModel


class Like(TimestampedModel):
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='like'
    )

    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='like'
    )

    def __str__(self):
        return f'{self.user} liked {self.recipe}'
