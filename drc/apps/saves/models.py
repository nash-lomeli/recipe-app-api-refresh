from django.db import models
from drc.apps.core.models import TimestampedModel	


class SaveRecipe(TimestampedModel):	

    recipe = models.ForeignKey(	
        'recipes.Recipe',	
        on_delete=models.CASCADE,	
        related_name='save_recipe'	
    )	

    user = models.ForeignKey(	
        'profiles.Profile',	
        on_delete=models.CASCADE,	
        related_name='save_recipe'	
    ) 