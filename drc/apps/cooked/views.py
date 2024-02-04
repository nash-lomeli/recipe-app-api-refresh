from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import models, serializers, renderers
from drc.apps.recipes import (models as recipe_models, 
    serializers as recipe_serializers, renderers as recipe_renderers
)

class CookedAPIView(views.APIView):
    serializer_class = recipe_serializers.RecipeSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (recipe_renderers.RecipeJSONRenderer,)

    def post(self, request, recipe_slug=None):
        user = self.request.user.profile
        context = {'request': request}

        try:
            recipe = recipe_models.Recipe.objects.get(slug=recipe_slug)
        except recipe_models.Recipe.DoesNotExist:
            raise TypeError('A recipe with this slug does not exist.')

        cooked = models.CookedRecipe.objects.filter(recipe=recipe, user=user)

        if cooked.exists():
            cooked.delete()
        else:
            models.CookedRecipe.objects.create(recipe=recipe, user=user)
        
        serializer = self.serializer_class(
            recipe,
            context=context,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CookedListAPIView(generics.ListAPIView):
    serializer_class = serializers.CookedListSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (renderers.CookedJSONRenderer,)

    def get_queryset(self):
        recipe_slug = self.kwargs['recipe_slug']

        recipe = recipe_models.Recipe.objects.get(slug=recipe_slug)

        queryset = models.CookedRecipe.objects.filter(recipe=recipe)
        return queryset

