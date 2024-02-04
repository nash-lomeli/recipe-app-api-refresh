from django.apps import AppConfig


class RecipesAppConfig(AppConfig):
    name = 'drc.apps.recipes'
    label = 'recipes'
    verbose_name = 'Recipes'

    def ready(self):
        import drc.apps.recipes.signals

default_app_config = 'drc.apps.recipes.RecipesAppConfig'
