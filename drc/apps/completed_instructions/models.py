from django.db import models
from drc.apps.core.models import TimestampedModel

class CompletedInstruction(TimestampedModel):
    instruction = models.ForeignKey(
        'recipes.Instruction',
        on_delete=models.CASCADE,
        related_name='completed_instruction'
    )

    user = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='completed_instruction'
    )

    def __str__(self):
        return f'{self.user} completed {self.instruction.id}'
