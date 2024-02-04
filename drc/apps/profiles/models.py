from django.db import models
from django.conf import settings

from drc.apps.core.models import TimestampedModel
from drc.apps.recipes import models as recipe_models

from django.db.models import Count


class Profile(TimestampedModel):
    print('PROFILES MODEL: class Profile(TimestampedModel)')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    name = models.CharField(blank=True, max_length=255)
    description = models.TextField(blank=True, max_length=255)
    street_address = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    state = models.CharField(blank=True, max_length=255)
    postal_code = models.CharField(blank=True, max_length=255)
    cuisine = models.CharField(max_length=255, blank=True, null=True)

    follow = models.ManyToManyField(
        'self',
        related_name='followed_by',
        blank=True,
        symmetrical=False,
    )

    def __str__(self):
        return self.user.email

    def following(self):
        return self.follow.count()

    def followers(self):
        return self.followed_by.count()
    
    def is_following(self, profile):
        return self.follow.filter(pk=profile.pk).exists()

    def is_follower(self, profile):
        return self.followed_by.filter(pk=profile.pk).exists()
    
    def has_like(self, recipe):
        return self.like.filter(recipe=recipe).exists()
    
    def has_cooked(self, recipe):
        return self.cooked_recipe.filter(recipe=recipe).exists()

    def has_completed(self, instruction):
        return self.completed_instruction.filter(instruction=instruction).exists()

    def recipe_note(self, recipe):
        return self.note_recipe.filter(recipe=recipe).first()
    
    def recipe_count(self):
        return self.recipes.count()

    def like_count(self):
        result = recipe_models.Recipe.objects.filter(author=self).aggregate(like_count=Count('like__id'))
        return result['like_count']

    def is_merchant(self):
        return self.user.groups.filter(name='Merchant').exists()
        