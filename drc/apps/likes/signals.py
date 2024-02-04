# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.core.cache import cache

# from . import models
# from src.apps.recipes import models as recipe_models

# @receiver(post_save, sender=models.Like)
# def post_save_like_cache(sender, instance, created, **kwargs):

#     recipe = recipe_models.Recipe.objects.get(pk=instance.recipe_id)
#     cache_key = f"recipe_details_{recipe.slug}_{instance.user_id}"
#     print('post_save_cache_key', cache_key)
#     cache.delete(cache_key)

#     print('post_save_cache_key - end')

# @receiver(post_delete, sender=models.Like)
# def post_delete_like_cache(sender, instance, **kwargs):

#     recipe = recipe_models.Recipe.objects.get(pk=instance.recipe_id)
#     cache_key = f"recipe_details_{recipe.slug}_{instance.user_id}"
#     print('post_delete_cache_cache_key', cache_key)
#     cache.delete(cache_key)

#     print('post_delete_cache - end')