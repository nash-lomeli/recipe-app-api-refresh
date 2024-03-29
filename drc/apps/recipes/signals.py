from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from drc.apps.core.utils import generate_random_string

from .models import Recipe

@receiver(pre_save, sender=Recipe)
def add_slug_to_recipe_if_not_exists(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255

    print('add_slug_to_recipe_if_not_exists')

    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = generate_random_string()

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')

            if len(parts) is 1:
                # The slug has no hypens. To append the unique string we must
                # arbitrarily remove `len(unique)` characters from the end of
                # `slug`. Subtract one to account for extra hyphen.
                slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = '-'.join(parts[:-1])

        instance.slug = slug + '-' + unique
